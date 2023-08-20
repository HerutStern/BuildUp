from django.db import models
from django.contrib.auth.models import User
from buildup_app.decorators import deleted_selector
from buildup_app.customized_fields import UpperCaseCharField
from buildup_app.validators import validate_building_permit_status, validate_role



# The Company Manager on signup creates the company while creating his own user.
# The company's project managers (the ones that open building permits),
# will add the company number of the company they work with on signup,
# so they will be associated with the company.
# project managers creating a new company meaning they won't be able to send their building permits
# to the company they work with.
# Companies can't see and work with other companies building permits.
class Company(models.Model):

    name = models.CharField(max_length=256, db_column='name', unique=True, null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)

    class Meta:
        db_table = 'company'

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f"{self.name} company"

# - Company Files -
# All the files that the company manager puts on the website,
# for the project managers to download if they need to.
# These are not the building permits files!!
# Just files that will be on the website,
# such as procedures forms, examples of construction plans and more...
class CompanyFile(models.Model):

    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                related_name='company_file')
    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
                            # The name for the file
    link = models.FileField(upload_to='company_file_uploads', max_length=256, db_column='link',
                            null=False, blank=False)

    class Meta:
        db_table = 'company_file'
        ordering = ['name']

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f"{self.name}"

# - Building Permits -
class BuildingPermit(models.Model):

    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                related_name='building_permit')
    user = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='user',
                             related_name='building_permit')
                            # This is the user who created the building permit,
                            # which is the project manager.
    name = models.CharField(max_length=256, db_column='name',unique=True, null=False, blank=False)
                            # This is the building permit name, not the user's or the company's name.
    creation_date = models.DateField(db_column='creation_date', auto_now_add=True)
    status = UpperCaseCharField(max_length=20, db_column="status", default='PENDING',
                                validators=[validate_building_permit_status])
    approval_date = models.DateField(db_column='approval_date', default=None, blank=True, null=True)

    class Meta:
        db_table = 'building_permit'
        ordering = ['creation_date']

    def __str__(self):
        return f'Permit - {self.name}, managed by {self.user.name}'


# - Sections Template -
# these are the sections the project manager will need to fill for sending a building permit.
# Each company has its own sections, that can be changed any time by the company manager
# (by changing column "is_deleted" or adding a new section)
class SectionTemplate(models.Model):

    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                related_name='section_template')
    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)

    class Meta:
        db_table = 'section_template'
        ordering = ['id']

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f'The section is - {self.name}'


# - Files Template -
# these are the files the project manager will need to add for sending a building permit.
# Each company has its own files, that can be changed any time by the company manager
# (by changing column "is_deleted" or adding a new file)
class FileTemplate(models.Model):

    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                related_name='file_template')
    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)

    class Meta:
        db_table = 'file_template'
        ordering = ['id']

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f'File - {self.name}'


# - Permits Sections -
# These are the sections, taken from the template, that are related to a building permit.
class BuildingPermitSection(models.Model):

    section_template = models.ForeignKey('SectionTemplate', on_delete=models.RESTRICT,
                                         db_column='section_template', related_name='building_permit_section')
    building_permit = models.ForeignKey('BuildingPermit', on_delete=models.RESTRICT,
                                        db_column='building_permit',  related_name='building_permit_section')
    name = models.CharField(max_length=256, db_column='name', null=False, blank=True)
                            # The name of the section may change in the future,
                            # so the original name of the section is saved,
                            # from when the building permit was created.
    content = models.CharField(max_length=500, db_column='content', null=False, blank=False)

    class Meta:
        db_table = 'building_permit_section'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} - {self.content}'


# - Permits Files -
# These are the files, taken from the template, that are related to a building permit.
class BuildingPermitFile(models.Model):

    file_template = models.ForeignKey('FileTemplate', on_delete=models.RESTRICT,
                                      db_column='file_template', related_name='building_permit_file')
    building_permit = models.ForeignKey('BuildingPermit', on_delete=models.RESTRICT,
                                        db_column='building_permit', related_name='building_permit_file')
    name = models.CharField(max_length=256, db_column='name', null=False, blank=True)
                            # The name of the file may change in the future,
                            # so the original name of the file is saved,
                            # from when the building permit was created.
    link = models.FileField(upload_to='building_permit_file_uploads', max_length=256, db_column='link',
                                    null=False, blank=False)

    class Meta:
        db_table = 'building_permit_file'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} of building permit number - {self.building_permit}'


# - Permissions -
# This table is organizing the roles users get when the company manager creates.
# Users permissions are all based on this role.
# In addition, the Building_Permits-Companies relation is managed here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.RESTRICT, db_column='user', related_name='profile')
    company = models.ForeignKey('Company', on_delete=models.RESTRICT,
                                db_column='company', related_name='profile')
    role = UpperCaseCharField(max_length=20, db_column='role', validators=[validate_role], null=False, blank=False)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return f'User number {self.user} from company number {self.company} is a {self.role}'

