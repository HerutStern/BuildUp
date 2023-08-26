from django.db import models
from django.contrib.auth.models import User
from buildup_app.decorators import deleted_selector
from buildup_app.customized_fields import UpperCaseCharField
from buildup_app.validators import validate_building_permit_status, validate_role


# Company:
class Company(models.Model):
    # On signup there will be a 'company name' input.
    # If the company does not exist, a new company will be opened,
    # and the user who signed up will be the company manager.
    # If the company exists, the user will be a project manager,
    # and he can send building permits to the company's 'company manager'.
    # Companies can't see and work with other company's information.

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


# Company Files:
class CompanyFile(models.Model):
    # These are not the building permits files!
    # Just files that will be on the website,
    # such as procedures forms, examples of construction plans and more...
    # The company manager can upload or delete files on his company, for the use of the project managers.
    # Project managers can not upload or delete those, they can only download the files.

    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                related_name='company_file')
    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
                                # The name of the file
    link = models.CharField(max_length=256, db_column='link', null=False, blank=False)

    class Meta:
        db_table = 'company_file'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


# Building Permits:
class BuildingPermit(models.Model):
    # Project manager opens a building permit,
    # Company manager sees the building permit and then can approve or reject it.

    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                related_name='building_permit')
    user = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='user',
                             related_name='building_permit')
                            # This is the user who created the building permit,
                            # which is the building permit's project manager
    name = models.CharField(max_length=256, db_column='name',unique=True, null=False, blank=False)
                            # This is the building permit name, not the user's or the company's name
    creation_date = models.DateField(db_column='creation_date', auto_now_add=True)
    status = UpperCaseCharField(max_length=20, db_column="status", default='PENDING',
                                validators=[validate_building_permit_status])
                                # Is changed when the company manager approves or rejects the building permit
    approval_date = models.DateField(db_column='approval_date', default=None, blank=True, null=True)
                                    # Is changed when the company manager approves the building permit

    class Meta:
        db_table = 'building_permit'
        ordering = ['creation_date']

    def __str__(self):
        return f'Permit - {self.name}, managed by {self.user.name}'


# Sections Templates:
class SectionTemplate(models.Model):
    # These are the sections that a project manager needs to fill on sending a new building permit.
    # Each company has its own sections, that can be changed any time by the company manager
    # (by changing column "is_deleted" or adding a new section).

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


# Files Templates:
class FileTemplate(models.Model):
    # These are the files that a project manager needs to upload on sending a new building permit.
    # Each company has its own files, that can be changed any time by the company manager
    # (by changing column "is_deleted" or adding a new file).

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


# Building Permit's Sections:
class BuildingPermitSection(models.Model):
    # These are the sections, that the project manager filled when he opened a new building permit.

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


# Building Permit's Files:
class BuildingPermitFile(models.Model):
    # These are the sections, that the project manager filled when he opened a new building permit.

    file_template = models.ForeignKey('FileTemplate', on_delete=models.RESTRICT,
                                      db_column='file_template', related_name='building_permit_file')
    building_permit = models.ForeignKey('BuildingPermit', on_delete=models.RESTRICT,
                                        db_column='building_permit', related_name='building_permit_file')
    name = models.CharField(max_length=256, db_column='name', null=False, blank=True)
                            # The name of the file may change in the future,
                            # so the original name of the file is saved,
                            # from when the building permit was created.
    link = models.CharField(max_length=256, db_column='link', null=False, blank=False)

    class Meta:
        db_table = 'building_permit_file'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} of building permit number - {self.building_permit}'


# Profiles:
class Profile(models.Model):
    # This model contains the role of each user, and the company they are related to,
    # so the Building_Permits-Companies relation is managed here.
    # User permissions are going to be based on their role.

    user = models.OneToOneField(User, on_delete=models.RESTRICT, db_column='user', related_name='profile')
    company = models.ForeignKey('Company', on_delete=models.RESTRICT,
                                db_column='company', related_name='profile')
    role = UpperCaseCharField(max_length=20, db_column='role', validators=[validate_role], null=False, blank=False)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return f'User number {self.user} from company number {self.company} is a {self.role}'
