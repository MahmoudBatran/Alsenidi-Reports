from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_report, name='upload_report'),
    path('', views.report_list, name='report_list'),
    path('register/', views.register, name='register'),
    path('manage_permissions/', views.manage_permissions, name='manage_permissions'),
]
