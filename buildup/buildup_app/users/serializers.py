from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from buildup_app.models import Company, Profile

# The three serializers for handling a user:

# Main user serializer -
class SignupSerializer(ModelSerializer):

    password = serializers.CharField(max_length=32, validators=[validate_password], write_only=True)
    company_name = serializers.CharField(max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'company_name']
        extra_kwargs = {
            'email': {'required': True}
        }
        validators = [UniqueTogetherValidator(User.objects.all(), ['email'])]

    def create(self, validated_data):
        with transaction.atomic():
            # Company and role: checking if the company exists -
            if Company.objects.filter(name=validated_data['company_name']).exists():
                # If the company exists, the user is a new project manager in this company
                company = get_object_or_404(Company, name=validated_data['company_name'])
                role = 'PROJECT_MANAGER'
            else:
                # If the company does not exist, this is a new company to create,
                # and the user is a company manager
                company = Company.objects.create(name=validated_data['company_name'])
                role = 'COMPANY_MANAGER'

            # Creating the user -
            user = User.objects.create_user(username=validated_data['username'],
                                       email=validated_data['email'],
                                            password=validated_data['password'])
            # Creating the profile -
            Profile.objects.create(company=company, user=user, role=role)

            return user

# Profile serializer -
class ProfileSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'role', 'company']
        model = Profile

# Company serializer -
class CompanySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Company
