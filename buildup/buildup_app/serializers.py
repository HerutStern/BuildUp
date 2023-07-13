from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from buildup_app.models import Company, Permission


# - Create Company Serializer -
class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model: Company
        fields = ['company_name']

    def create(self, validated_data):
        company = Company.objects.create(**validated_data)
        company.save()
        return company

# - Sign-Up Serializer -
# This will be used for two views functions:
# 1 - <the_function_name> - opening an account for a new manager,
#   while also creating a new company.
# 2 - <the_function_name> - for the manager to add a new company worker.
#
# * You can't open a new account without opening a new company.
# * Only the company manager can create new accounts for company workers.
class SignupSerializer(ModelSerializer):

    password = serializers.CharField(
        max_length=32, validators=[validate_password], write_only=True)
    company_name = serializers.CharField(max_length=64, write_only=True)
    role = serializers.CharField(max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'company_name', 'role']
        extra_kwargs = {
            'email': {'required': True},
            # 'username': {'read_only': True}
        }
        validators = [UniqueTogetherValidator(User.objects.all(), ['email'])]
    def create(self, validated_data):
        company = Company.objects.create(company_name=validated_data['company_name'])
        user = User.objects.create(username=validated_data['username'],
                                   email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Permission.objects.create(company=company, user=user, role=validated_data['role'])
        return user




