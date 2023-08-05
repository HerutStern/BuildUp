from rest_framework import serializers

from buildup_app.models import FileTemplate


class FileTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTemplate
        fields = '__all__'

