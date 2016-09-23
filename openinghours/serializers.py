
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from .models import Rule


MIN_TIME = 0
MAX_TIME = 24*60

INVALID_FORMAT_MSG = _('Invalid time format. Must be %h:%m.')


def time_string_to_minutes(value):
    try:
        hour_str, minute_str = value.split(':')
    except:
        raise serializers.ValidationError(INVALID_FORMAT_MSG)

    try:
        hour = int(hour_str)
        minute = int(minute_str)
    except ValueError:
        raise serializers.ValidationError(INVALID_FORMAT_MSG)
    return 60 * hour + minute


class RuleSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Rule
        fields = ('id', 'day', 'open', 'close', 'nr', )
        list_serializer_class = BulkListSerializer

    def validate_open(self, value):
        open = time_string_to_minutes(value)
        if open < MIN_TIME:
            raise serializers.ValidationError(_('Opening time cannot be negative.'))

        return value

    def validate_close(self, value):
        close = time_string_to_minutes(value)

        if close > MAX_TIME:
            raise serializers.ValidationError(_('Closing time greater than 24*60 minutes'))

        return value

    def validate(self, data):
        open = time_string_to_minutes(data.get('open'))
        close = time_string_to_minutes(data.get('close'))

        if open >= close:
            raise serializers.ValidationError(_('Closing time is earlier than the opening time.'))

        return data


