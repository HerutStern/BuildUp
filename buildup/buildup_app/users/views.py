from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from buildup_app.models import Company, Permission
from buildup_app.users.serializers import SignupSerializer


# - Sign-Up Function -
#
# permissions:
# 1 - opening an account for a new manager, while also creating the new company.
# 2 - for the manager to add a new company worker.
#
# * You can't open a new account without opening a new company.
# * Only the company manager can create new accounts for  his company workers.
@api_view(['POST'])
def signup(request):
    new_user = SignupSerializer(data=request.data)
    new_user.is_valid(raise_exception=True)
    new_user.save()
    return Response(data=new_user.data, status=status.HTTP_202_ACCEPTED)




# - Getting User Information Function -
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_information(request):
    serializer = SignupSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# - Getting All Company Users -
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_company_users(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    permissions = Permission.objects.filter(company=company)
    users = [permission.user for permission in permissions]

    serializer = SignupSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['DELETE'])
def user_delete(request, user_id):

    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    return Response({'message': f"User '{user.username}' has been deactivated."},
                    status=status.HTTP_202_ACCEPTED)
