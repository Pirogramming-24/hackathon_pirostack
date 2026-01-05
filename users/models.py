from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    role = models.CharField(max_length=10, default="empty_role")
    nickname = models.CharField(max_length=20, default="empty_nickname")
    name = models.CharField(max_length=10, default="empty_name")
    phone_number = models.CharField(max_length=10, default="010-0000-0000")
    password = models.CharField(max_length=20, default="empty_code")
    
    def __str__(self):
        return f'{self.user.username} Profile'