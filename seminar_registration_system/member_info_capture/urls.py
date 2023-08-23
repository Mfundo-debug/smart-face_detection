from django.urls import path
from member_info_capture import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('member_info_capture/', views.member_info_capture, name='member_info_capture'),
    path('find_user/', views.find_user, name='find_user'),
    path('member_info_capture_success/', TemplateView.as_view(template_name='member_info_capture/member_info_capture_success.html'), name='member_info_capture_success'),
    
]