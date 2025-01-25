from django.urls import path
from customer_management.views import list_users

urlpatterns = [
    path('users', list_users, name='list_users')
]