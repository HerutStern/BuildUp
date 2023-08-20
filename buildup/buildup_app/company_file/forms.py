from django import forms
from buildup_app.company_file.validators import validate_file_type, validate_file_size
from buildup_app.models import CompanyFile

# Upload files - for CompanyFile
class CompanyFileForm(forms.ModelForm):

    class Meta:
        model = CompanyFile
        fields = '__all__'

        # A Note About Fields-
        # It is strongly recommended to explicitly set all fields
        # that should be edited in the form using the fields attribute.
        # Failure to do so can easily lead to security problems
        # when a form unexpectedly allows a user to set certain fields,
        # especially when new fields are added to a model

        extra_kwargs = {
            'file_link': {
                'validators': [validate_file_type, validate_file_size],
            }
        }