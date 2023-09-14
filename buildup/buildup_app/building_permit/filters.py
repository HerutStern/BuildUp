import django_filters
from django.contrib.auth.models import User
from buildup_app.models import BuildingPermit


class BuildingPermitFilterSet(django_filters.FilterSet):

    id = django_filters.NumberFilter(method='filter_by_id')
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
    def filter_by_id(queryset, name, value): # We will filter both matching id's
                                             # and id's containing the value.
                                             # value of id '3' can return both id '3' and id '13'
        # Filtering both exact matches and id's containing the value -
        exact_matches = queryset.filter(id=value) # Exact matches
        partial_matches = queryset.filter(id__icontains=value) # Partial matches

        # Combining both filtered query-sets -
        queryset = exact_matches | partial_matches

        # Returning the combined queryset -
        return queryset.distinct() # The distinct() is ensuring that the queryset
                                   # only contains unique objects,
                                   # because of the combining of the two query-sets.

    # Name filter -
    @staticmethod
    def filter_by_name(queryset, name, value): # We will filter both matching names
                                               # and names containing the value
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
    def filter_by_project_manager(queryset, name, value): # We will filter both matching names
                                                          # and names containing the value
        # Filtering both exact matches and usernames containing the value -
        exact_matches = User.objects.filter(username=value)  # Exact matches
        partial_matches = User.objects.filter(username__icontains=value)  # Partial matches

        # Combining both filtered query-sets -
        filtered_users_list = exact_matches | partial_matches

        # Filtering the queryset based on the users in the filtered users list -
        queryset = queryset.filter(user__in=filtered_users_list)

        # Returning the filtered queryset -
        return queryset.distinct() # The distinct() is ensuring that the queryset
                                   # only contains unique objects,
                                   # because of the combining of the two query-sets.
