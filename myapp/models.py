from django.db import models

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class HouseOwner(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneno = models.BigIntegerField()
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pincode = models.BigIntegerField()
    district = models.CharField(max_length=100)
    idproof = models.CharField(max_length=100)
    Aadhar = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default='')


class User(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneno = models.BigIntegerField()
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pincode = models.BigIntegerField()
    district = models.CharField(max_length=100)
    idproof = models.CharField(max_length=100)
    Aadhar = models.CharField(max_length=100)



class Complaint(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=100)
    date = models.DateField()
    reply = models.CharField(max_length=100)
    status = models.CharField(max_length=100)


class Home(models.Model):
    OWNER = models.ForeignKey(HouseOwner, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)
    rental_amount = models.CharField(max_length=100)
    proof = models.CharField(max_length=100)
    phoneno = models.IntegerField()
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pincode = models.BigIntegerField()
    district = models.CharField(max_length=100)
    property_type = models.CharField(max_length=100)
    rental_period = models.CharField(max_length=100)
    area_sqft = models.CharField(max_length=100)
    rooms = models.CharField(max_length=100)
    bathrooms = models.CharField(max_length=100)
    furnishing = models.CharField(max_length=100)
    parking = models.CharField(max_length=100)
    kitchen = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    latitude = models.CharField(max_length=100,default="")
    longitude = models.CharField(max_length=100,default="")
    reqstatus = models.CharField(max_length=100)

class Request(models.Model):
    HOME = models.ForeignKey(Home,on_delete=models.CASCADE)
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField()
    rental_period = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Review(models.Model):
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    # HOME = models.ForeignKey(Home,on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.CharField(max_length=100)
    review = models.CharField(max_length=100)


class Payment(models.Model):
    REQUEST = models.ForeignKey(Request,on_delete=models.CASCADE)
    date = models.DateField()
    amount=models.CharField(max_length=100)
    status=models.CharField(max_length=100)



