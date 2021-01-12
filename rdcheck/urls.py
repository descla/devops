from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'rdcheck'
urlpatterns = [
    path('',views.index, name='index'),
    path('linux', views.linux_roundcheck, name='linux'),
]
