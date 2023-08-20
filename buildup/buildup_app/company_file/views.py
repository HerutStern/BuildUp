from django.db import transaction
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from buildup_app.company_file.forms import CompanyFileForm
from buildup_app.company_file.serializers import CompanyFileSerializer
from buildup_app.models import CompanyFile, Profile
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer


# A note about company files -
# The manager can upload or delete files on his company, for the use of the company users.
# All the other users can not upload or delete those, they can just watch (or download) the files.

class PageClass(PageNumberPagination):
    page_size = 10
    # page_query_param = 'bbb'
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

    def get_queryset(self):
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

            # Recreating request.data with the company id -
            data_copy = request.data.copy()
            serializer_data = data_copy
            additional_data = {'company': company_serializer.data['id']}
            new_data = {**serializer_data, **additional_data}
            updated_post_data = QueryDict(mutable=True)
            updated_post_data.update(new_data)
            updated_files_data = MultiValueDict(request.FILES)

            # Creating file -
            form = CompanyFileForm(updated_post_data, updated_files_data)
            form.is_valid()
            form = form.save()
            company_file = get_object_or_404(CompanyFile, id=form.id)
            serializer = CompanyFileSerializer(company_file)
            return Response(serializer.data)


