from django.urls import path, re_path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('datasets/', views.map_list, name='maps'),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    url(r'^logout/$',LogoutView.as_view(), name='logout'),
    path('upload/select_type', views.select_file_type, name='select_file_type'),
    path('upload/map_picker', views.map_picker, name='map_picker'),
    path('upload/location_handler', views.location_handler, name='location_handler'),
    path('datasets/<int:pk>/', views.detail, name='detail'),
    path('success', views.success, name='success'),
    url(r'^search/$', views.search, name='search'),
]