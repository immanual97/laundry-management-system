from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ClothType(models.Model):
    clothtypes = models.CharField(max_length=25)

class ServiceType(models.Model):
    servicetypes = models.CharField(max_length=25)
    price = models.IntegerField()

class Address(models.Model):
    address = models.CharField(max_length=250)
    userid = models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING)

class OrderNumber(models.Model):
    userid = models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING)
    orders = models.IntegerField(default=0)

class Status(models.Model):
    status = models.CharField(max_length=25)

class Orders(models.Model):
    date = models.DateField()
    clothtype = models.CharField(max_length=25,default=None)
    noofclothes = models.IntegerField()
    cost = models.IntegerField(default=0)
    discound = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)
    statusid = models.ForeignKey(Status,default=None,on_delete=models.DO_NOTHING)
    servicetypes = models.CharField(max_length=25,default=0)
    homedelivery = models.BooleanField(default=False)
    serviceid = models.ForeignKey(ServiceType,default=None,on_delete=models.DO_NOTHING)
    userid = models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING)

class Discounds(models.Model):
    discounds = models.IntegerField(default=0)
    orders = models.IntegerField(default=0)

class Payment(models.Model):
    payed = models.BooleanField()
    orderid = models.ForeignKey(Orders,default=None,on_delete=models.DO_NOTHING)

class Feedback(models.Model):
    userid = models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=500,default=0)