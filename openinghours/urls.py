from rest_framework_bulk.routes import BulkRouter
from .views import RulesViewSet

router = BulkRouter()
router.register(r'openinghours', RulesViewSet)
