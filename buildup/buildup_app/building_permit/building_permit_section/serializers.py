from rest_framework import serializers
from buildup_app.models import BuildingPermitSection


class BuildingPermitSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPermitSection
        fields = '__all__'
