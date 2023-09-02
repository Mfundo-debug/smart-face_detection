from django.urls import path, include
from member_info_capture import views
from django.views.generic import TemplateView
from rest_framework import routers
from .views import MemberViewSet, MemberInfoCaptureViewSet


router = routers.DefaultRouter()
router.register('member', MemberViewSet)
router.register('member_info_capture', MemberInfoCaptureViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.landing_page, name='landing_page'),
    path('member_info_capture/', views.member_info_capture, name='member_info_capture'),
    path('find_user/', views.find_user, name='find_user'),
    path('member_info_capture_success/', TemplateView.as_view(template_name='member_info_capture/member_info_capture_success.html'), name='member_info_capture_success'),
    path('validate_information/', views.validate_information, name='validate_information'),
    path('validate_information_success/', TemplateView.as_view(template_name='member_info_capture/validate_information_success.html'), name='validate_information_success'),
    
    
]