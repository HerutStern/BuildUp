from django.db import transaction
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from buildup_app.company_file.forms import CompanyFileForm
from buildup_app.company_file.serializers import CompanyFileSerializer
from buildup_app.models import CompanyFile, Profile
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer


class PageClass(PageNumberPagination):
    page_size = 20
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

            # Adding the company id and handling files data -
            data_copy = request.data.copy()
            serializer_data = data_copy
            additional_data = {'company': company_serializer.data['id']}
            new_data = {**serializer_data, **additional_data}
            updated_post_data = QueryDict(mutable=True)
            updated_post_data.update(new_data)
            updated_files_data = MultiValueDict(request.FILES)

            # Creating the file with the updated data -
            form = CompanyFileForm(updated_post_data, updated_files_data)
            form.is_valid()
            form = form.save()

            # Return serialized data -
            company_file = get_object_or_404(CompanyFile, id=form.id)
            serializer = CompanyFileSerializer(company_file)
            return Response(serializer.data)
