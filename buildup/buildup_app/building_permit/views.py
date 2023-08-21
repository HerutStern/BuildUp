import datetime
from django.db import transaction
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from buildup_app.building_permit.building_permit_file.serializers import BuildingPermitFileSerializer
from buildup_app.building_permit.building_permit_section.serializers import BuildingPermitSectionSerializer
from buildup_app.building_permit.serializers import BuildingPermitSerializer
from buildup_app.models import Profile, BuildingPermit, BuildingPermitFile, BuildingPermitSection
from buildup_app.permissions import BuildingPermitApprovalPermission
from buildup_app.users.serializers import CompanySerializer, SignupSerializer


class BuildingPermitViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = BuildingPermitSerializer
    permission_classes = [IsAuthenticated, BuildingPermitApprovalPermission]
    queryset = BuildingPermit.objects.all()

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        company = profile.company
        company_serializer = CompanySerializer(company)
        company_id = company_serializer.data['id']
        queryset = self.queryset.filter(company=company_id)
        return queryset

    def create(self, request, *args, **kwargs): # Right after using this 'create' function on UI,
                                                # BuildingPermitFileViewSet and BuildingPermitSectionViewSet
                                                # 'create' functions will be used
                                                # with the new building permit ID,
                                                # to complete the building permit creation
        with transaction.atomic():
            data_copy = request.data.copy()
            user_serializer = SignupSerializer(instance=request.user)
            profile = get_object_or_404(Profile, user=request.user)
            company = profile.company
            company_serializer = CompanySerializer(instance=company)

            data_copy = {
                'name': data_copy['name'],
                'user': user_serializer.data['id'],
                'company': company_serializer.data['id']
            }
            
            serializer = self.get_serializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        permit_data = serializer.data
        for permit in permit_data:
            files = BuildingPermitFile.objects.filter(building_permit=permit['id'])
            files_data = BuildingPermitFileSerializer(instance=files, many=True).data
            permit['files'] = files_data

            sections = BuildingPermitSection.objects.filter(building_permit=permit['id'])
            sections_data = BuildingPermitSectionSerializer(instance=sections, many=True).data
            permit['sections'] = sections_data

        if page is not None:
            return self.get_paginated_response(permit_data)

        else:
            return Response(permit_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data_copy = request.data.copy()
        if data_copy['status'] in ['APPROVED', 'REJECTED']:
            data_copy['approval_date'] = datetime.date.today()

        serializer = self.get_serializer(instance, data=data_copy, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
