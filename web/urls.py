from django.conf import settings
from django.views import static
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^level/$', views.LevelListView.as_view()),
    url(r'^level/(?P<pk>[0-9a-z]{40})$', views.LevelView.as_view()),
    url(r'^level/(?P<pk>[0-9a-z]{40})/validate/$', views.Validate.as_view()),

    url(r'^$', static.serve, {'path':'templates/base.html', 'document_root': settings.STATIC_ROOT}),
    url(r'^(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
]
