from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^view_all/', views.view_all, name ='view_all'),
    url(r'^used_materials/', views.used_materials, name='used_materials'),
    url(r'^select_date/', views.SelectDate.as_view(), name='select_date'),
    url(r'^materials_form_submission/', views.materials_form_submission, name='materials_form_submission'),
    url(r'^clock_in_form_submission/', views.clock_in_form_submission, name='clock_in_form_submission'),
    url(r'^clock_out_form_submission/', views.clock_out_form_submission, name='clock_out_form_submission'),
    url(r'^schedule', views.schedule_view, name='schedule')
]