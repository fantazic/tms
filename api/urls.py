from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^me/$', views.me, name='me'),
    url(r'^crud_task/$', views.crud_task, name='crudTask'),
    url(r'^get_dates_and_tasks/$', views.get_dates_and_tasks, name='getDatesAndTasks'),
    url(r'^set_hour/$', views.set_hour, name='setHour'),
    url(r'^export/$', views.export, name='export'),
]
