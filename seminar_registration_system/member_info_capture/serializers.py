from rest_framework import serializers
from .models import MemberInfoCapture

class MemberInfoCaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberInfoCapture
        fields = '__all__'