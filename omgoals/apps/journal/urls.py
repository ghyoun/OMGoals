from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.journal, name='journal'),
    url(r'^addjournal$', views.add_journal, name='add_journal')
]
