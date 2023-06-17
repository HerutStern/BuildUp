from django.db import models

from buildup.buildup_app.validators import validate_delete


class Companies(models.Model):

    company_name = models.CharField(max_length=256, db_column='company_name',
                                    null=False, blank=False)
    delete = models.BooleanField(db_column='delete', null=True, blank=True,
                                 validators=validate_delete)

    class Meta:
        db_table = 'companies'

    def __str__(self):
        return self.company_name

class BuildingPermits(models.Model):

    company_id = models.ForeignKey('Companies', on_delete=models.RESTRICT)
    building_permit_name = models.CharField(max_length=256, db_column='building_permit_name',
                                    null=False, blank=False)
    delete = models.BooleanField(db_column='delete', null=True, blank=True,
                                 validators=validate_delete)

    class Meta:
        db_table = 'building_permits'

    def __str__(self):
        return self.building_permit_name

class CompanyFiles(models.Model):

    company_id = models.ForeignKey('Companies', on_delete=models.RESTRICT)
    file_name = models.CharField(max_length=256, db_column='file_name',
                                    null=False, blank=False)
    file_link = models.CharField(max_length=256, db_column='file_link', null=False, blank=False)
    delete = models.BooleanField(db_column='delete', null=True, blank=True,
                                 validators=validate_delete)

    class Meta:
        db_table = 'company_files'


