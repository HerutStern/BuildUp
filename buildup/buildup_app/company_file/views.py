from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from buildup_app.company_file.serializers import CompanyFileSerializer
from buildup_app.files_handler.upload_files import upload
from buildup_app.models import CompanyFile, Profile
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer


class PageClass(PageNumberPagination):
    page_size = 50
    # page_query_param = ''

class CompanyFileViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = CompanyFileSerializer
    pagination_class = PageClass
    permission_classes = [IsAuthenticated, ManagerPermission]
    queryset = CompanyFile.objects.all()

    def get_queryset(self): # Filtering the queryset to user's company data only
        profile = get_object_or_404(Profile, user=self.request.user)
        company = profile.company
        company_serializer = CompanySerializer(company)
        company_id = company_serializer.data['id']
        queryset = self.queryset.filter(company=company_id)
        return queryset


    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            # Getting user company -
            profile = get_object_or_404(Profile, user=request.user)
            company = profile.company
            company_serializer = CompanySerializer(company)

            # Uploading File -
            blob = upload(request=request, folder='company_files') # The function 'upload' returns the blob

            # Updating data -
            data_copy = request.data.copy()
            data_copy['company'] = company_serializer.data['id']
            data_copy['link'] = blob.public_url

            # Returning serialized data -
            serializer = self.get_serializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
