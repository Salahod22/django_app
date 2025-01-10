# data_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('access/<int:entry_id>/', views.access_data, name='access_data'), 
    path('analyze/<int:entry_id>/', views.analyze_data, name='analyze_data'),
    path('visualize/<int:entry_id>/', views.visualize_data, name='visualize_data'),
    path('data/', views.data_list, name='data_list'),
]