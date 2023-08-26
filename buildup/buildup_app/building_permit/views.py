import datetime
from django.db import transaction
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from buildup_app.building_permit.building_permit_file.serializers import BuildingPermitFileSerializer
from buildup_app.building_permit.building_permit_section.serializers import BuildingPermitSectionSerializer
from buildup_app.building_permit.filters import BuildingPermitFilterSet
from buildup_app.building_permit.serializers import BuildingPermitSerializer
from buildup_app.models import Profile, BuildingPermit, BuildingPermitFile, BuildingPermitSection
from buildup_app.permissions import BuildingPermitApprovalPermission
from buildup_app.users.serializers import CompanySerializer, SignupSerializer

class PageClass(PageNumberPagination):
    page_size = 30
    # page_query_param = ''

class BuildingPermitViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = BuildingPermitSerializer
    pagination_class = PageClass
    permission_classes = [IsAuthenticated, BuildingPermitApprovalPermission]
    queryset = BuildingPermit.objects.all()
    filterset_class = BuildingPermitFilterSet

    def get_queryset(self): # Filtering the queryset to user's company data only
        profile = get_object_or_404(Profile, user=self.request.user)
        company = profile.company
        company_serializer = CompanySerializer(company)
        company_id = company_serializer.data['id']
        queryset = self.queryset.filter(company=company_id)
        return queryset

    def create(self, request, *args, **kwargs):
        # A note about the creation process -
        # Right after using this 'create' function on UI,
        # BuildingPermitFileViewSet and BuildingPermitSectionViewSet 'create' functions will be used
        # with this new building permit ID, to complete the building permit creation.

        with transaction.atomic():
            # Getting the user's company -
            profile = get_object_or_404(Profile, user=request.user)
            company = profile.company

            # Company and user serializers -
            company_serializer = CompanySerializer(instance=company)
            user_serializer = SignupSerializer(instance=request.user)

            # Recreating the data containing the creating user and his company -
            data_copy = request.data.copy()
            data_copy = {
                'name': data_copy['name'],
                'user': user_serializer.data['id'],
                'company': company_serializer.data['id']
            }

            # Serializing the updated data and creating the new building permit -
            serializer = self.get_serializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs): # Returning a costumed list,
                                              # with each building permit's sections and files.
                                              # The list is used on the UI for showing
                                              # each building permit's information,
                                              # so it is easier handling a list already
                                              # containing each building permits information

        # Serializing data, the queryset is based on the page -
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # For each building permit data adding the building permit's files and sections -
        for building_permit_data in serialized_data:
            # Adding files -
            files = BuildingPermitFile.objects.filter(building_permit=building_permit_data['id'])
            files_data = BuildingPermitFileSerializer(instance=files, many=True).data
            building_permit_data['files'] = files_data

            # Adding sections -
            sections = BuildingPermitSection.objects.filter(building_permit=building_permit_data['id'])
            sections_data = BuildingPermitSectionSerializer(instance=sections, many=True).data
            building_permit_data['sections'] = sections_data

        # Return updated data (a paginated response or not) -
        if page is not None:
            return self.get_paginated_response(serialized_data)
        else:
            return Response(serialized_data)

    def update(self, request, *args, **kwargs): # The 'update' function will be used for
                                                # company manager approving or rejecting a building permit

        # Getting the building permit the view is displaying -
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Updating approval date if the building permit has been approved -
        data_copy = request.data.copy()
        if data_copy['status'] in ['APPROVED', 'REJECTED']:
            data_copy['approval_date'] = datetime.date.today()

        # Serializing the partial data and updating -
        serializer = self.get_serializer(instance, data=data_copy, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Finishing 'update' view-set function -
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
