from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from buildup_app.building_permit.serializers import BuildingPermitSerializer
from buildup_app.file_template.serializers import FileTemplateSerializer
from buildup_app.models import Profile, FileTemplate, BuildingPermit
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer, SignupSerializer, ProfileSerializer


class BuildingPermitViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = BuildingPermitSerializer
    permission_classes = [IsAuthenticated]
    queryset = BuildingPermit.objects.all()

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        company = profile.company
        company_serializer = CompanySerializer(company)
        company_id = company_serializer.data['id']
        queryset = self.queryset.filter(company=company_id)
        return queryset

    def create(self, request, *args, **kwargs):
        user_serializer = SignupSerializer(instance=request.user)
        profile = get_object_or_404(Profile, user=request.user)
        company = profile.company
        company_serializer = CompanySerializer(instance=company)
        data = {
            'name': request.data['name'],
            'user': user_serializer.data['id'],
            'company': company_serializer.data['id']
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)