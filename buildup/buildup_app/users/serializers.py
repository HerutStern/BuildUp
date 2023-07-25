from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from buildup_app.models import Company, Permission
from buildup_app.validators import validate_roles_options





# - Sign-Up Serializer -
class SignupSerializer(ModelSerializer):

    password = serializers.CharField(
        max_length=32, validators=[validate_password], write_only=True)
    company_name = serializers.CharField(max_length=64, write_only=True)
    role = serializers.CharField(max_length=64, write_only=True, validators=[validate_roles_options])

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'company_name', 'role']
        extra_kwargs = {
            'email': {'required': True}
        }
        validators = [UniqueTogetherValidator(User.objects.all(), ['email'])]
    def create(self, validated_data):
        with transaction.atomic():
            company = Company.objects.create(company_name=validated_data['company_name'])
            user = User.objects.create_user(username=validated_data['username'],
                                       email=validated_data['email'],
                                            password=validated_data['password'])
            Permission.objects.create(company=company, user=user, role=validated_data['role'])
        return user

# class PermissionDetailsSerializer(ModelSerializer):
#     user = SignupSerializer()
#     class Meta:
#         fields = '__all__'
#         model = Permission
#

