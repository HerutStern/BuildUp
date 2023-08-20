from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from buildup_app.models import Profile
from buildup_app.users.serializers import SignupSerializer, ProfileSerializer, CompanySerializer



@api_view(['POST', 'GET']) # GET method is for development uses
def signup(request):
    user = None
    user_serializer = None

    # User serializer -
    if request.method == 'POST':
        user_serializer = SignupSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

    elif request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_serializer = SignupSerializer(instance=user)


    # Profile serializer -
    profile = get_object_or_404(Profile, user=user)
    profile_serializer = ProfileSerializer(instance=profile)

    # Company serializer -
    company = profile.company
    company_serializer = CompanySerializer(instance=company)

    # Serializing the data from each serializer
    user_data = user_serializer.data
    profile_data = profile_serializer.data
    company_data = company_serializer.data


    # Creating a dictionary containing the serialized data from all serializers
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

        # Creating a dictionary containing the serialized data from all serializers
        data = {
            'user': user_data,
            'company': company_data,
            'profile': profile_data
        }
        return Response(data=data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': f"User '{user.username}' has been deactivated."},
                        status=status.HTTP_410_GONE)


