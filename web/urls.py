from django.conf import settings
from django.views import static
from django.conf.urls import url

from .views import Validate


urlpatterns = [
    url(r'^validate/$', Validate.as_view()),

    url(r'^$', static.serve, {'path':'templates/base.html', 'document_root': settings.STATIC_ROOT}),
    url(r'^(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
]