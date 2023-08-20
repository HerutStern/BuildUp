from rest_framework import serializers

from buildup_app.models import BuildingPermit


class BuildingPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPermit
        fields = '__all__'


