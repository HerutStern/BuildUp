from rest_framework.exceptions import ValidationError

# Models validators:
def validate_building_permit_status(value): # Building permit statuses
    statuses_list = ['PENDING', 'APPROVED', 'REJECTED']
    if value not in statuses_list:
        raise ValidationError(f'{value} is not a valid status choice.')

def validate_role(value): # User roles
    roles_list = ['COMPANY_MANAGER', 'PROJECT_MANAGER']
    if value not in roles_list:
        raise ValidationError(f'{value} is not a valid role choice.')


# Files validators:
def validate_file_type(value): # Allowed file types
    allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
    # Check:
    if value.content_type not in allowed_types:
        raise ValidationError('Invalid file type. Only JPEG, PNG, and PDF files are allowed.')

def validate_file_size(value): # Maximum allowed file size (in bytes)
    max_size = 10 * 1024 * 1024  # 10 MB
    # Check:
    if value.size > max_size:
        raise ValidationError('File size exceeds the allowed limit. Maximum size is 10 MB.')
