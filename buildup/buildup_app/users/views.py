from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from buildup_app.models import Profile
from buildup_app.users.serializers import SignupSerializer, ProfileSerializer, CompanySerializer

@api_view(['POST'])
def signup(request):
    with transaction.atomic():
        # User serializer -
        user_serializer = SignupSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # Profile serializer -
        profile = get_object_or_404(Profile, user=user_serializer.data['id'])
        profile_serializer = ProfileSerializer(instance=profile)

        # Company serializer -
        company = profile.company
        company_serializer = CompanySerializer(instance=company)

        # Serializing the data from each model
        user_data = user_serializer.data
        profile_data = profile_serializer.data
        company_data = company_serializer.data

        # Creating a data containing the serialized data from all models
        data = {
            'user': user_data,
            'company': company_data,
            'profile': profile_data
        }

        return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def user(request):
    if request.method == 'GET':
        # User serializer -
        user_serializer = SignupSerializer(instance=request.user)

        # Profile serializer -
        profile = get_object_or_404(Profile, user=request.user)
        profile_serializer = ProfileSerializer(instance=profile)

        # Company serializer -
        company = profile.company
        company_serializer = CompanySerializer(instance=company)

        # Serializing the data from each serializer
        user_data = user_serializer.data
        profile_data = profile_serializer.data
        company_data = company_serializer.data

        # Creating a data containing the serialized data from all models
        data = {
            'user': user_data,
            'company': company_data,
            'profile': profile_data
        }
        return Response(data=data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE': # Instead of deleting, changing field is_active to 'False'
        the_user = request.user
        the_user.is_active = False
        the_user.save()
        return Response({'message': f"User '{the_user.username}' has been deactivated."},
                        status=status.HTTP_410_GONE)
