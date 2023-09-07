import django_filters
from django.contrib.auth.models import User
from buildup_app.models import BuildingPermit


class BuildingPermitFilterSet(django_filters.FilterSet):

    id = django_filters.NumberFilter(field_name='id')
    building_permit_name = django_filters.CharFilter(method='filter_by_name')
    status = django_filters.CharFilter(field_name='status')
    project_manager = django_filters.CharFilter(method='filter_by_project_manager'
                                                ) # Expecting the username of the project manager user
    creation_date = django_filters.DateFilter(field_name='creation_date')
    approval_date = django_filters.DateFilter(field_name='approval_date')

    class Meta:
        model = BuildingPermit
        fields = '__all__'

    # Name filter -
    @staticmethod
    def filter_by_name(queryset, name, value): # We will filter both matching names
                                               # and names containing the name
        # Filtering both exact matches and names containing the value -
        exact_matches = queryset.filter(name=value) # Exact matches
        partial_matches = queryset.filter(name__icontains=value) # Partial matches

        # Combining both filtered query-sets -
        queryset = exact_matches | partial_matches

        # Returning the combined queryset -
        return queryset.distinct() # The distinct() is ensuring that the queryset
                                   # only contains unique objects,
                                   # because of the combining of the two query-sets.

    # Project manager filter -
    @staticmethod
    def filter_by_project_manager(queryset, name, value):
        try:
            # Getting the user by the project manager name -
            user = User.objects.get(username=value)

            # Filtering the queryset by the user's id -
            queryset = queryset.filter(user=user.id)

            # Returning the filtered queryset -
            return queryset

        # If the specified username does not correspond to an existing user in User.objects.get(),
        # an error would occur. return an empty queryset to avoid raising an error.
        except User.DoesNotExist:
            return queryset.none()
