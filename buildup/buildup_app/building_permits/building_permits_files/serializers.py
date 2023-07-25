from rest_framework import serializers
from buildup_app.models import PermitFile


class PermitFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermitFile
        fields = '__all__'

