from django.db import models
from django.contrib.auth.models import User

from buildup_app.decorators import deleted_selector
from buildup_app.fields_classes import UpperCaseCharField
from buildup_app.validators import validate_status_options, validate_roles_options


# - Company -
# The Company Manager creates the company and his own user
# and he is the one who will create the company's workers users after.
# You can't open your own user, it will mean that you opened a new company.
# If you work for a specific company, the company manager will create your user.
# Creating a new company meaning you won't be able to work with the other company DB.
# Companies can't see and work with other companies building permits.
# Each company has its own DB.
class Company(models.Model):
    company_name = models.CharField(max_length=256, db_column='company_name', null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)

    class Meta:
        db_table = 'company'

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f"{self.company_name} company"
    def __repr__(self):
        return f"\nFrom The Table 'company':\n" \
               f"id - {self.pk}\n" \
               f"company_name - {self.company_name}\n" \
               f"is_deleted - {self.is_deleted}\n"


# - Company Files -
# All the files that the company manager put on the website, for the workers to download.
# *** It is not the building permits files table!
# Just files that will be on the website, such as procedures forms, examples of construction plans and more...
class CompanyFile(models.Model):
    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                   related_name='company_file', related_query_name='company_file')
    file_name = models.CharField(max_length=256, db_column='file_name', null=False, blank=False)
    file_link = models.CharField(max_length=256, db_column='file_link', null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)
    class Meta:
        db_table = 'company_file'

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f"File {self.file_name} - {self.file_link}"
    def __repr__(self):
        return f"\nFrom The Table 'company_file':\n" \
               f"id - {self.pk}\n" \
               f"company_id - {self.company}\n" \
               f"file_name - {self.file_name}\n" \
               f"file_link - {self.file_link}\n" \
               f"is_deleted - {self.is_deleted}\n"


# - Building Permits -
# The statuses and approvals of the building permits have their own Tables.
class BuildingPermit(models.Model):
    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                   related_name='building_permit', related_query_name='building_permit')
    project_manager_user_id = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='project_manager_user_id',
                                                related_name='building_permit', related_query_name='building_permit')
    building_permit_name = models.CharField(max_length=256, db_column='building_permit_name',
                                    null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)
    class Meta:
        db_table = 'building_permit'

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f'Permit - {self.building_permit_name}, managed by {self.project_manager_user_id.name}'
    def __repr__(self):
        return f"\nFrom The Table 'building_permit':\n" \
               f"id - {self.pk}\n" \
               f"company_id - {self.company}\n" \
               f"project_manager_user_id - {self.project_manager_user_id}\n" \
               f"building_permit_name - {self.building_permit_name}\n" \
               f"is_deleted - {self.is_deleted}\n"


# - Permits Statuses -
# The statuses rows are being created any time the permit changes its status,
# the user who changed the status will go to the 'user_id' section.
# the 'user_id' section will be completed when the user changed the permit to the next status,
# So 'user_id' might be null.
# On the Signatures_Round status, there will be created one row for each user_id who needs to sign,
# so as long as they are not all approved, we know it won't change to the next status.
# There are might be other people who will approve the permit,
# instead of the user_id that have been chosen (such as the company manager),
# but the user_id will not change. It just means they signed the permit on his behalf. Just like a Rubber Stamp.
class PermitStatus(models.Model):
    building_permit = models.ForeignKey('BuildingPermit', on_delete=models.RESTRICT, db_column='building_permit',
                                   related_name='permit_status', related_query_name='permit_status')
    status = UpperCaseCharField(max_length=256, validators=[validate_status_options], db_column='status')
    start_date = models.DateField(db_column='start_date', auto_now_add=True,
                                  null=False, blank=False)  # The date the row was created (won't change on updates)
    approving_user_id = models.ForeignKey(User, on_delete=models.RESTRICT, validators=[validate_status_options],
                                         db_column='approving_user_id', related_name='permits_statuses',
                                         related_query_name='permit_status')
    is_approved = models.BooleanField(db_column='is_approved', default=False)
    class Meta:
        db_table = 'permit_status'
    def __str__(self):
        return f'\nPermit {self.building_permit.building_permit_name}\n' \
               f'Status - {self.status}\n' \
               f'Date started - {self.start_date.__str__()}\n'
    def __repr__(self):
        return f"\nFrom The Table 'permit_status':\n" \
               f"id - {self.pk}\n" \
               f"permit_id - {self.building_permit}\n" \
               f"status - {self.status}\n" \
               f"start_date - {self.start_date}\n" \
               f"approving_user_id - {self.approving_user_id}\n" \
               f"is_approved - {self.is_approved}\n"


# - Sections Template -
# these are the sections the project manager will need to fill for sending a building permit.
# Each company has its own sections, that can be changed any time by the company manager
# (by changing column "is_deleted" or adding a new section)
class SectionsTemplate(models.Model):
    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                   related_name='sections_template', related_query_name='section_template')
    section_name = models.CharField(max_length=256, db_column='section_name',
                                    null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)
    class Meta:
        db_table = 'sections_template'
    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f'Section - {self.section_name}'
    def __repr__(self):
        return f"\nFrom The Table 'sections_template':\n" \
               f"id - {self.pk}\n" \
               f"company_id - {self.company}\n" \
               f"section_name - {self.section_name}\n" \
               f"is_deleted - {self.is_deleted}\n"


# - Files Template -
# these are the files the project manager will need to add for sending a building permit.
# Each company has its own files, that can be changed any time by the company manager
# (by changing column "is_deleted" or adding a new file)
class FilesTemplate(models.Model):
    company = models.ForeignKey('Company', on_delete=models.RESTRICT, db_column='company',
                                   related_name='files_template', related_query_name='file_template')
    file_name = models.CharField(max_length=256, db_column='file_name',
                                    null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)
    class Meta:
        db_table = 'files_template'
    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f'File - {self.file_name}'
    def __repr__(self):
        return f"\nFrom The Table 'files_template':\n" \
               f"id - {self.pk}\n" \
               f"company_id - {self.company}\n" \
               f"file_name - {self.file_name}\n" \
               f"is_deleted - {self.is_deleted}\n"


# - Permits Sections -
# These are the sections, taken from the template, that are related to a building permit.
class PermitSection(models.Model):

    sections_template = models.ForeignKey('SectionsTemplate', on_delete=models.RESTRICT, db_column='sections_template',
                                    related_name='permit_section', related_query_name='permit_section',
                                    null=False, blank=False)
    content = models.CharField(max_length=600, db_column='content',
                                    null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)
    class Meta:
        db_table = 'permit_section'

    @deleted_selector
    def __str__(self, sentence):
        if self.is_deleted:
            return sentence
        else:
            return f'{self.sections_template.section_name} - {self.content}'
    def __repr__(self):
        return f"\nFrom The Table 'permit_section':\n" \
               f"id - {self.pk}\n" \
               f"template_id - {self.sections_template}\n" \
               f"content - {self.content}\n" \
               f"is_deleted - {self.is_deleted}\n"


# - Permits Files -
# These are the files, taken from the template, that are related to a building permit.
class PermitFile(models.Model):
    files_template = models.ForeignKey('FilesTemplate', on_delete=models.RESTRICT,  db_column='files_template',
                                   related_name='permit_file', related_query_name='permit_file')
    file_link = models.CharField(max_length=256, db_column='file_link',
                                    null=False, blank=False)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)
    class Meta:
        db_table = 'permits_file'
    def __str__(self):
        return self.file_link
    def __repr__(self):
        return f"\nFrom The Table 'file':\n" \
               f"id - {self.pk}\n" \
               f"template_id - {self.files_template}\n" \
               f"file_link - {self.file_link}\n" \
               f"is_deleted - {self.is_deleted}\n"

# - Permissions -
# This table is organizing the roles users get when the company manager creates.
# Users permissions are all based on this role.
# In addition, the Building_Permits-Companies relation is managed here.
class Permission(models.Model):

    user = models.ForeignKey(User, on_delete=models.RESTRICT, validators=[validate_status_options],
                                          db_column='user', related_name='permission',
                                          related_query_name='permission')
    company = models.ForeignKey('Company', on_delete=models.RESTRICT,  db_column='company',
                                   related_name='permission', related_query_name='permission')
    role = UpperCaseCharField(max_length=256, db_column='role', validators=[validate_roles_options],
                            null=False, blank=False)
    class Meta:
        db_table = 'permission'
    def __str__(self):
        return self.role
    def __repr__(self):
        return f"\nFrom The Table 'Permission':\n" \
               f"id - {self.pk}\n" \
               f"user_id - {self.user}\n" \
               f"company_id - {self.company}\n" \
               f"role - {self.role}\n"
