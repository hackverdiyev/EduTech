from django.db import models
from base.models import Account

class Group(models.Model):
    name=models.CharField(max_length=100)
    about=models.CharField(max_length=1000, blank=True)
    subject=models.CharField(max_length=20)
    creator=models.ForeignKey(Account,on_delete=models.CASCADE)
    admins=models.CharField(max_length=1000000000,default='%')
    participants=models.CharField(max_length=100000000000000000000,default='%')
    requests=models.CharField(max_length=100000000000000000000,default='%')
    contests=models.CharField(max_length=10000,default='%')
    pub_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Contest(models.Model):
    name=models.CharField(max_length=100)
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    creator=models.ForeignKey(Account,on_delete=models.CASCADE)
    problems=models.CharField(max_length=10000,default='%')
    pub_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Discussion(models.Model):
    message=models.CharField(max_length = 10000)
    contest=models.ForeignKey(Contest,on_delete=models.CASCADE)
    user_added=models.ForeignKey(Account,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.contest.name