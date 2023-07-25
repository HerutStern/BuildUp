from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from buildup_app.company_files.forms import CompanyFileForm
from buildup_app.company_files.serializers import CompanyFileSerializer
from buildup_app.models import CompanyFile

# A note about company files -
# The manager can upload or delete files on his company, for the use of the company users.
# All the other users can not upload or delete those, they can just watch (or download) the files.

# The manager is adding a new company file:
@api_view(['POST'])
def add_company_file(request):
    if request.method == 'POST':
        form = CompanyFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


# Get a specific file:
@api_view(['GET'])
def get_company_file_by_id(request, company_file_id):
    company_file = get_object_or_404(CompanyFile, pk=company_file_id)
    serializer = CompanyFileSerializer(company_file)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get all company files:
@api_view(['GET'])
def get_company_files_by_company_id(request, company_id):
    company_files = CompanyFile.objects.filter(company_id=company_id)
    if not company_files:
        return Response({'error': 'Company not found or no files associated with the company.'},
                        status=status.HTTP_404_NOT_FOUND)
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(company_files, request)
    serializer = CompanyFileSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
