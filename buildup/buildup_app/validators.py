from rest_framework.exceptions import ValidationError


def validate_building_permit_status(value):
    statuses_list = ['PENDING', 'APPROVED', 'REJECTED']
    if value not in statuses_list:
        raise ValidationError(f'{value} is not a valid status choice.')

def validate_role(value):
    statuses_list = ['COMPANY_MANAGER', 'PROJECT_MANAGER']
    if value not in statuses_list:
        raise ValidationError(f'{value} is not a valid role choice.')