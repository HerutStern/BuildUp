from rest_framework import serializers
from buildup_app.models import CompanyFile


class CompanyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFile
        fields = '__all__'

