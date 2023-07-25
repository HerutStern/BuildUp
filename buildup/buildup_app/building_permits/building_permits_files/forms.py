from django import forms
from buildup_app.company_files.validators import validate_file_type, validate_file_size
from buildup_app.models import PermitFile

# Upload files - for PermitFile
class PermitFileForm(forms.ModelForm):

    class Meta:
        model = PermitFile

        fields = '__all__'
        extra_kwargs = {
            'file_link': {
                'validators': [validate_file_type, validate_file_size],
            }
        }

