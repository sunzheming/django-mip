from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url



urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('maps/', views.map_list, name='maps'),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    url(r'^logout/$',LogoutView.as_view(), name='logout'),
#     path('<str:filepath>/', views.download_file),
    path('maps/<str:filename>', views.download, name='file_link'),
    path('test/', views.test_page, name='test_page'),
]