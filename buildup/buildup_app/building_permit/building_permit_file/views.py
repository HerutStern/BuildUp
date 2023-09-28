from django.db import transaction
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from buildup_app.building_permit.building_permit_file.serializers import BuildingPermitFileSerializer
from buildup_app.files_handler.upload_files import upload
from buildup_app.models import FileTemplate, BuildingPermitFile


class BuildingPermitFileViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = BuildingPermitFileSerializer
    permission_classes = [IsAuthenticated]
    queryset = BuildingPermitFile.objects.all()

    def create(self, request, *args, **kwargs): # This is used for finishing the building permit creation process
        with transaction.atomic():
            # Adding file template name to data -
            data_copy = request.data.copy()
            file_template = get_object_or_404(FileTemplate, id=data_copy['file_template'])
            data_copy['name'] = file_template.name

            # Uploading File -
            blob = upload(request=request, folder="building_permit_files") # The function 'upload' returns the blob

            # Updating data -
            data_copy['link'] = blob.public_url

            # Returning serialized data -
            serializer = self.get_serializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
