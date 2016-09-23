
from rest_framework.viewsets import ModelViewSet
from .models import Rule
from .serializers import RuleSerializer
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import BulkModelViewSet

# ListBulkCreateUpdateDestroyAPIView


class RulesViewSet(BulkModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
