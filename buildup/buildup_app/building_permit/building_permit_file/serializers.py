from rest_framework import serializers
from buildup_app.models import BuildingPermitFile


class BuildingPermitFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPermitFile
        fields = '__all__'
