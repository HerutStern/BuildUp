from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from buildup_app.file_template.serializers import FileTemplateSerializer
from buildup_app.models import Profile, SectionTemplate
from buildup_app.permissions import ManagerPermission
from buildup_app.users.serializers import CompanySerializer

class SectionTemplateViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = FileTemplateSerializer
    permission_classes = [IsAuthenticated, ManagerPermission]
    queryset = SectionTemplate.objects.all()

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        company = profile.company
        company_serializer = CompanySerializer(company)
        company_id = company_serializer.data['id']
        queryset = self.queryset.filter(company=company_id, is_deleted=False)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_410_GONE)
