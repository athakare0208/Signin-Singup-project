from django.db import models
from django.contrib.auth.models import User  
# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    contact = models.CharField(max_length=10, null=True)
    branch = models.CharField(max_length=30, null=True)
    dob = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=6, null=True)
    role = models.CharField(max_length=15, null=True)   
    age = models.IntegerField(null=True)  

    def __str__(self):
        return self.user.username 

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uploadingdate = models.CharField(max_length=30, null=True, default='unknown')
    branch = models.CharField(max_length=100, null=True, default='default_branch')    
    subject = models.CharField(max_length=30, null=True, default='default_subject')
    notefile = models.FileField(default='default_file.txt')
    filetype = models.CharField(max_length=30, default='unknown')
    description = models.CharField(max_length=200, default='No description provided') 
    status = models.CharField(max_length=15, default='unknown')
    dateofbirth = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=6, null=True)  

    def __str__(self):
        return self.user.username + " - " + str(self.status) 