from django.db import models
from django.utils.translation import ugettext_lazy as _
from .formats import parse_rules

WEEKDAYS = (
    ('mon', _('Monday')),
    ('tue', _('Tuesday')),
    ('wed', _('Wednesday')),
    ('thu', _('Thursday')),
    ('fri', _('Friday')),
    ('sat', _('Saturday')),
    ('sun', _('Sunday'))
)


class RuleManager(models.Manager):

    def create_from_facebook_data(self, data):
        parsed_rules = parse_rules(data)
        instances = [self.model(**r) for r in parsed_rules]
        self.bulk_create(instances)


class Rule(models.Model):
    open = models.CharField(verbose_name=_('Opening time'), max_length=5,
                            default='00:00')
    close = models.CharField(verbose_name=_('Closing time'), max_length=5,
                             default='24:00')
    day = models.CharField(max_length=3, choices=WEEKDAYS)
    nr = models.PositiveSmallIntegerField(default=1)

    objects = RuleManager()

    class Meta:
        verbose_name = _('Opening hours rule')
        verbose_name_plural = _('Opening hours rules')

    def __str__(self):
        return '{0} {1}-{2}'.format(self.get_day_display(), self.open, self.close)
        
    __unicode__ = __str__
