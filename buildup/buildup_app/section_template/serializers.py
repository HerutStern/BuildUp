from rest_framework import serializers

from buildup_app.models import SectionTemplate


class SectionTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionTemplate
        fields = '__all__'