from django.db import transaction
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from buildup_app.building_permit.building_permit_file.forms import BuildingPermitFileForm
from buildup_app.building_permit.building_permit_file.serializers import BuildingPermitFileSerializer
from buildup_app.building_permit.building_permit_section.serializers import BuildingPermitSectionSerializer
from buildup_app.building_permit.serializers import BuildingPermitSerializer
from buildup_app.file_template.serializers import FileTemplateSerializer
from buildup_app.models import Profile, FileTemplate, BuildingPermit, BuildingPermitFile, BuildingPermitSection, \
    SectionTemplate
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer, SignupSerializer, ProfileSerializer


class BuildingPermitSectionViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = BuildingPermitSectionSerializer
    permission_classes = [IsAuthenticated]
    queryset = BuildingPermitSection.objects.all()

    def create(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        section_template = get_object_or_404(SectionTemplate, id=data_copy['section_template'])
        section_template_name = section_template.name
        data_copy['name'] = section_template_name

        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)