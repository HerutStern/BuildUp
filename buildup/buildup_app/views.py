
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from buildup_app.serializers import SignupSerializer, CreateCompanySerializer


# - Sign-Up Function -
@api_view(['POST'])
def signup_new_company(request):
    new_user = SignupSerializer(data=request.data)
    new_user.is_valid(raise_exception=True)
    print(new_user.validated_data)

    new_user.save()

    return Response(data=new_user.data)


# - Getting User Information Function -
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_information(request):
    serializer = SignupSerializer(instance=request.user)
    return Response(serializer.data)



