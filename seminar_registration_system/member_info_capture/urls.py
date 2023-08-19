from django.urls import path
from . import views

urlpatterns = [
    path('member_info_capture/', views.member_info_capture, name='member_info_capture'),
    
]