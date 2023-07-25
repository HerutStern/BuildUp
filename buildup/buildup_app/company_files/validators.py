from rest_framework.exceptions import ValidationError


# Allowed file types -
def validate_file_type(value):
    allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
    # Check:
    if value.content_type not in allowed_types:
        raise ValidationError('Invalid file type. Only JPEG, PNG, and PDF files are allowed.')


# Maximum allowed file size (in bytes) -
def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 MB
    # Check:
    if value.size > max_size:
        raise ValidationError('File size exceeds the allowed limit. Maximum size is 10 MB.')
