from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('result/<int:pk>/', views.result, name='result'),
    path('history/', views.history, name='history'),


    path('contact/', views.contact, name='contact'),
    path('download/<int:pk>/', views.download_result, name='download_result'),
    path('delete/<int:pk>/', views.delete_analysis, name='delete_analysis'),
    path('clear_history/', views.clear_history, name='clear_history'),
    path('clear-my-history/', views.clear_my_history, name='clear_my_history'),
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
    # Admin Dashboard URLs
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-analyses/', admin_views.admin_analyses, name='admin_analyses'),

    path('admin-users/', admin_views.admin_users, name='admin_users'),
    path('admin-analytics/', admin_views.admin_analytics, name='admin_analytics'),
] 