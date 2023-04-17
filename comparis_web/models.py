from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

from comparis import settings


class Properties(models.Model):
    prop_id = models.CharField(unique=True, max_length=255, null=False)
    title = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    streetnumber = models.CharField(max_length=255, null=True)
    postalcode = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    price = models.IntegerField(null=True)
    pricetypetext = models.CharField(max_length=255, null=True)
    propertytypetext = models.CharField(max_length=255, null=True)
    area = models.CharField(max_length=255, null=True)
    imageurls = models.TextField(null=True)
    foundforthefirsttime = models.DateField(blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    onlinestatus = models.CharField(max_length=255, null=True)
    remarks = models.TextField(null=True)
    partnername = models.CharField(max_length=255, null=True)
    room = models.FloatField(null=True)
    floor = models.CharField(max_length=255, null=True)
    livingspace = models.CharField(max_length=255, null=True)
    yearofconstruction = models.CharField(max_length=255, null=True)
    availabledate = models.CharField(max_length=255, null=True)
    isoldbuilding = models.CharField(max_length=255, null=True)
    vendor_name = models.CharField(max_length=255, null=True)
    vendor_phone = models.CharField(max_length=255, null=True)
    property_url = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
