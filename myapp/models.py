from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    dob=models.DateField()
    photo=models.FileField()
    phone=models.BigIntegerField()
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)

class ServiceProvider(models.Model):
    name=models.TextField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    dob=models.DateField()
    photo=models.FileField()
    phone=models.BigIntegerField()
    gender=models.CharField(max_length=100)
    servicetype=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='pending')
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)

class Request(models.Model):
    SERVICEPROVIDER=models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)
    latitude=models.FloatField()
    longitude=models.FloatField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.IntegerField()
    status=models.CharField(max_length=100)
    date=models.DateTimeField()
    Problem=models.TextField()
    amount=models.FloatField(default=0)

class Complaints(models.Model):
    REQUEST=models.ForeignKey(Request,on_delete=models.CASCADE)
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)
    complaints=models.TextField()
    polarity=models.CharField(max_length=100)
    status=models.TextField(default='pending')
    date=models.DateTimeField()



