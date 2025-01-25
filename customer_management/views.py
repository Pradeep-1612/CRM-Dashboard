from django.db.models import Q
from .models import AppUser, Address, CustomerRelationship
from django.http import JsonResponse


# CustomerRelationship focused code
def list_users(request):
    # Extract search parameters from the request's GET query string
    search_params = request.GET
    sort_by = request.GET.get('sort', 'id')  # Default sorting by 'id'
    range_filter = request.GET.get('range', None)  # Range filter for pagination (e.g., 0-100)

    # Parse the range filter for pagination (offset-limit)
    limit = 100  # Default limit to 100
    offset = 0   # Default offset to 0
    if range_filter:
        try:
            offset, endValue = map(int, range_filter.split('-'))
            limit = endValue - offset + 1
        except ValueError:
            return JsonResponse({"error": "Invalid 'range' format. Expected 'offset-limit'."}, status=400)

    # Build the Q object for dynamic searching across AppUser, Address, and CustomerRelationship
    search_filter = Q()

    # Iterate over the query parameters to build dynamic filters for AppUser, Address, and CustomerRelationship
    for key, value in search_params.items():
        # Skip non-search parameters like 'sort' and 'range'
        if key == 'sort' or key == 'range':
            continue

        # Search in CustomerRelationship fields
        if hasattr(CustomerRelationship, key):
            search_filter &= Q(**{f"{key}__icontains": value})  # Case-insensitive search for CustomerRelationship fields

        # Search in AppUser fields (through the ForeignKey relationship)
        elif hasattr(AppUser, key):
            search_filter &= Q(**{f"appuser__{key}__icontains":value})  # Case-insensitive search for AppUser fields

        # Search in Address fields (through the ForeignKey relationship)
        elif hasattr(Address, key):
            search_filter &= Q(**{f"appuser__address__{key}__icontains":value})  # Case-insensitive search for Address fields
        else:
            return JsonResponse({"error": f"Invalid query parameter '{key}'. Please input valid query parameter."}, status=400)

    try:
        # Perform the query with the search filters, including related Address and CustomerRelationship data
        cstmr_rlts = CustomerRelationship.objects.filter(search_filter).select_related('appuser', 'appuser__address')
    
        # Sorting: Apply sorting by the specified field
        formattedSortAttribute = get_formatted_sorting_param(sort_by)
        if(formattedSortAttribute): 
            cstmr_rlts = cstmr_rlts.order_by(formattedSortAttribute)

        # Apply pagination: Limit and offset
        cstmr_rlts_paginated = cstmr_rlts[offset:offset + limit]
    except Exception as e:
        return JsonResponse({"error": f"Error while processing filters, sorting, or pagination: {str(e)}"}, status=400)

    cstmr_rlts_data = []
    for cstmr_rlt in cstmr_rlts_paginated:
        # Prepare the cstmr_rlts data dictionary
        cstmr_rlt_details = {
            "id": cstmr_rlt.appuser.id,
            "first_name": cstmr_rlt.appuser.first_name,
            "last_name": cstmr_rlt.appuser.last_name,
            "gender": cstmr_rlt.appuser.gender,
            "customer_id": cstmr_rlt.appuser.customer_id,
            "phone_number": cstmr_rlt.appuser.phone_number,
            "created": cstmr_rlt.appuser.created,
            "birthday": cstmr_rlt.appuser.birthday,
            "last_updated": cstmr_rlt.appuser.last_updated,
            "address": {
                "id": cstmr_rlt.appuser.address.id,
                "street": cstmr_rlt.appuser.address.street,
                "street_number": cstmr_rlt.appuser.address.street_number,
                "city_code": cstmr_rlt.appuser.address.city_code,
                "city": cstmr_rlt.appuser.address.city,
                "country": cstmr_rlt.appuser.address.country,
            },
            "customer_relationship": {
                "id": cstmr_rlt.id,
                "points": cstmr_rlt.points,
                "created": cstmr_rlt.created,
                "last_activity": cstmr_rlt.last_activity
            }
        }

        # Append the user details to the response list
        cstmr_rlts_data.append(cstmr_rlt_details)

    # Prepare the response data with nested structure for Address and CustomerRelationship
    final_data = {
        "customer_relationships": cstmr_rlts_data,
        "total_count": cstmr_rlts.count(),  # Total number of users matching the filter
        "limit": limit,
        "offset": offset,
    }

    return JsonResponse(final_data)

def get_formatted_sorting_param(sortAttribute):
    columnName = sortAttribute
    formattedSortAttribute = sortAttribute # Ascending order
    sortBySymbol = ''
    
    if sortAttribute:
        if sortAttribute.startswith('-'):
            columnName = sortAttribute[1:]
            sortBySymbol = '-'
        elif sortAttribute.startswith('+'):
            columnName = sortAttribute[1:]
            formattedSortAttribute = sortAttribute[1:] # Descending order

        # Search in AppUser fields (through the ForeignKey relationship)
        if hasattr(AppUser, columnName):
            formattedSortAttribute = sortBySymbol + 'appuser__' + columnName

        # Search in Address fields (through the ForeignKey relationship)
        elif hasattr(Address, columnName):
            formattedSortAttribute = sortBySymbol + 'appuser__address__' + columnName
    
    return formattedSortAttribute



'''
# Users focused code

def list_users(request):
    # Extract search parameters from the request's GET query string
    search_params = request.GET
    sort_by = request.GET.get('sort', 'id')  # Default sorting by 'id'
    range_filter = request.GET.get('range', None)  # Range filter for pagination (e.g., 0-100)

    # Parse the range filter for pagination (offset-limit)
    limit = 100  # Default limit to 100
    offset = 0   # Default offset to 0
    if range_filter:
        try:
            offset, limit = map(int, range_filter.split('-'))
        except ValueError:
            offset, limit = 0, 100  # Default to offset=0, limit=100 if range is incorrectly formatted

    # Build the Q object for dynamic searching across AppUser, Address, and CustomerRelationship
    search_filter = Q()

    # Iterate over the query parameters to build dynamic filters for AppUser, Address, and CustomerRelationship
    for key, value in search_params.items():
        # Skip non-search parameters like 'sort' and 'range'
        if key == 'sort' or key == 'range':
            continue

        # Search in AppUser fields
        if hasattr(AppUser, key):
            search_filter &= Q(**{f"{key}__icontains": value})  # Case-insensitive search for AppUser fields

        # Search in Address fields (through the ForeignKey relationship)
        elif hasattr(Address, key):
            search_filter &= Q(**{f"address__{key}__icontains":value})  # Case-insensitive search for Address fields

        # Search in CustomerRelationship fields (through the ForeignKey relationship)
        elif hasattr(CustomerRelationship, key):
            search_filter &= Q(**{f"customerrelationship__{key}__icontains":value})  # Case-insensitive search for CustomerRelationship fields
    # Perform the query with the search filters, including related Address and CustomerRelationship data
    users = AppUser.objects.filter(search_filter).select_related('address').prefetch_related('customerrelationship_set')

    # Sorting: Apply sorting by the specified field
    if sort_by:
        if sort_by.startswith('-'):
            users = users.order_by(sort_by)  # Descending order
        elif sort_by.startswith('+'):
            users = users.order_by(sort_by[1:])  # Ascending order
        else:
            users = users.order_by(sort_by)

    # Apply pagination: Limit and offset
    users_paginated = users[offset:offset + limit]
    user_data = []
    for user in users_paginated:
        # Prepare the user data dictionary
        user_details = {
            "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "gender": user.gender,
                "customer_id": user.customer_id,
                "phone_number": user.phone_number,
                "created": user.created,
                "birthday": user.birthday,
                "last_updated": user.last_updated,
                "address": {
                    "id": user.address.id,
                    "street": user.address.street,
                    "street_number": user.address.street_number,
                    "city_code": user.address.city_code,
                    "city": user.address.city,
                    "country": user.address.country,
                },
                "customer_relationships": {}
        }

        # Access all related CustomerRelationships and add them to the response
        for relationship in user.customerrelationship_set.all():
            user_details["customer_relationships"] = {
                "id": relationship.id,
                "points": relationship.points,
                "created": relationship.created,
                "last_activity": relationship.last_activity
            }

        # Append the user details to the response list
        user_data.append(user_details)

    # Prepare the response data with nested structure for Address and CustomerRelationship
    final_data = {
        "users": user_data,
        "total_count": users.count(),  # Total number of users matching the filter
        "limit": limit,
        "offset": offset,
    }

    return JsonResponse(final_data)
'''