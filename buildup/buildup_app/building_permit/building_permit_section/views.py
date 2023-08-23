from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from buildup_app.building_permit.building_permit_section.serializers import BuildingPermitSectionSerializer
from buildup_app.models import BuildingPermitSection, SectionTemplate


class BuildingPermitSectionViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = BuildingPermitSectionSerializer
    permission_classes = [IsAuthenticated]
    queryset = BuildingPermitSection.objects.all()

    def create(self, request, *args, **kwargs): # This is used to finish the building permit creation process
        # Adding section template name to data -
        data_copy = request.data.copy()
        section_template = get_object_or_404(SectionTemplate, id=data_copy['section_template'])
        data_copy['name'] = section_template.name

        # Serializing the updated data and creating the new building permit section -
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
