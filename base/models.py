from django.db import models

class Account(models.Model):
    username=models.CharField(max_length=20)
    fullname=models.CharField(max_length=100,blank=True)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    profile_photo=models.ImageField(upload_to='profile_photos/', default='profile_photos/default_pp.png')
    point=models.IntegerField(default=0)
    admin_tag=models.BooleanField(default=False)
    teacher_tag=models.BooleanField(default=False)
    clever_tag=models.BooleanField(default=False)
    olympian_tag=models.BooleanField(default=False)
    groups=models.CharField(max_length=1000000,default='%')
    requests=models.CharField(max_length=1000000,default='%')
    def __str__(self):
        return self.username

class Verification(models.Model):
    username=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50,blank=True)
    fullname=models.CharField(max_length=100,blank=True)
    six_digit_code=models.IntegerField()
    time=models.BigIntegerField()
    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.CharField(max_length=1200)
    message=models.CharField(max_length=1000000)
    def __str__(self):
        return self.email