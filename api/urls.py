from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^me/$', views.me, name='me'),
    url(r'^update_task/$', views.update_task, name='updateTask'),
    url(r'^add_task/$', views.add_task, name='addTask'),
    url(r'^get_tasks/$', views.get_tasks, name='getTasks'),
    url(r'^get_dates/$', views.get_dates, name='getDates'),
    url(r'^set_hour/$', views.set_hour, name='setHour'),
    url(r'^export/$', views.export, name='export'),
]
