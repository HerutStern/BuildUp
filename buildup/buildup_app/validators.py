from django.core.exceptions import ValidationError


def validate_name(value):
    if type(value) is not str:
        raise ValidationError(f'{value} is not a String type')
    if len(value) > 256:
        raise ValidationError

def validate_status_options(value):
    statuses_list = ['EDITING', 'QUALITY_CHECK', 'SIGNATURES_ROUND', 'FINAL_APPROVAL', 'APPROVED', 'CANCELLED']
    if value not in statuses_list:
        raise ValidationError(f'{value} is not a valid status choice.')

def validate_roles_options(value):
    roles_list = ['QUALITY_CHECKER', 'PERMIT_INSPECTOR', 'FINAL_APPROVAL', 'COMPANY_MANAGER', 'PROJECT_MANAGER']
    if value not in roles_list:
        raise ValidationError(f'{value} is not a valid role choice.')
