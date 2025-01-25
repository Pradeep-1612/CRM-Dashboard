from django.db import models

# @author Pradeep Juturu

# CRM models

class Address(models.Model):
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=50)
    city_code = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class AppUser(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)  # Index on first_name
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    customer_id = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, db_column='address_id')
    birthday = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

class CustomerRelationship(models.Model):
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE, db_column='appuser_id')
    points = models.IntegerField(db_index=True)  # Index on points
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField()

