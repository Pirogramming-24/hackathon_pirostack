from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)

    role = models.CharField(max_length=10, default="empty_role")
    nickname = models.CharField(max_length=20, default="empty_nickname")
    name = models.CharField(max_length=10, default="empty_name")
    phone_number = models.CharField(max_length=10, default="010-0000-0000")
    password = models.CharField(max_length=20, default="empty_code")
    permission = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # 유저가 새로 생성(created=True)될 때만 프로필을 만듭니다.
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # 유저가 저장될 때 프로필도 같이 저장되게 합니다.
    instance.profile.save()