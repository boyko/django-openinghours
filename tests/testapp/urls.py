from django.conf.urls import include, url
from django.contrib import admin
from openinghours.urls import router as openinghours_router


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(openinghours_router.urls))
]
