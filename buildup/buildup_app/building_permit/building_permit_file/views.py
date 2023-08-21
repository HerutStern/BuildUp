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
from buildup_app.building_permit.serializers import BuildingPermitSerializer
from buildup_app.file_template.serializers import FileTemplateSerializer
from buildup_app.models import Profile, FileTemplate, BuildingPermit, BuildingPermitFile
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer, SignupSerializer, ProfileSerializer


class BuildingPermitFileViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = BuildingPermitFileSerializer
    permission_classes = [IsAuthenticated]
    queryset = BuildingPermitFile.objects.all()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data_copy = request.data.copy()
            file_template = get_object_or_404(FileTemplate, id=data_copy['file_template'])
            file_template_name = file_template.name
            data_copy['name'] = file_template_name

            files_data = MultiValueDict(request.FILES)
            # Creating file -
            form = BuildingPermitFileForm(data_copy, files_data)
            form.is_valid()
            form = form.save()
            file = get_object_or_404(BuildingPermitFile, id=form.id)
            serializer = BuildingPermitFileSerializer(file)
            return Response(serializer.data)