from django.db import transaction
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from buildup_app.file_template.serializers import FileTemplateSerializer
from buildup_app.models import Profile, FileTemplate
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer


class FileTemplateViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = FileTemplateSerializer
    permission_classes = [IsAuthenticated, ManagerPermission]
    queryset = FileTemplate.objects.all()

    def get_queryset(self): # Filtering the queryset to user's company data only
        profile = get_object_or_404(Profile, user=self.request.user)
        company = profile.company
        company_serializer = CompanySerializer(company)
        company_id = company_serializer.data['id']
        queryset = self.queryset.filter(company=company_id, is_deleted=False)
        return queryset

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            # Getting the user's company -
            profile = get_object_or_404(Profile, user=request.user)
            company = profile.company
            company_serializer = CompanySerializer(company)

            # Recreating data with the user's company id -
            data_copy = request.data.copy()
            data_copy['company'] = company_serializer.data['id']

            # Serializing the updated data and creating the new file template -
            serializer = self.get_serializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def destroy(self, request, *args, **kwargs):  # Instead of deleting, changing field is_deleted to 'True'
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_410_GONE)
