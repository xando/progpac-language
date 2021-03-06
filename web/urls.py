from django.conf import settings
from django.views import static
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^level/$', views.LevelsList.as_view()),
    url(r'^level/(?P<key>[0-9a-z]+)/$', views.Level.as_view()),
    url(r'^$', static.serve, {'path':'templates/base.html', 'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns.append(
        url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
    )
