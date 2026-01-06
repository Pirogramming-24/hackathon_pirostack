from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    role = models.CharField(max_length=10, default="empty_role")
    name = models.CharField(max_length=10, default="empty_name")
    phone_number = models.CharField(max_length=15, default="010-0000-0000")
    password = models.CharField(max_length=128, default="empty_code")
    permission = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        # Allows using django.contrib.auth.decorators.login_required with Profile
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_username(self):
        return self.phone_number
