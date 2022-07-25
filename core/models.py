from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime

class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, firstName, lastName, password):
        """ Create a new user profile """
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, firstName=firstName, lastName=lastName)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, firstName, lastName, password):
        """ Create a new superuser profile """
        user = self.create_user(email,firstName, lastName, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    firstName = models.CharField(max_length=255, default="", blank=True)
    lastName = models.CharField(max_length=255, default="", blank=True)
    nickName = models.CharField(max_length=255, default="", blank=True)
    password = models.CharField(max_length=255, default="", blank=True)
    birthDate = models.DateField(null=True, default=None)
    sex = models.CharField(max_length=255, default="", blank=True)
    institution = models.CharField(max_length=255, default="", blank=True)
    province = models.CharField(max_length=255, default="", blank=True)
    municipality = models.CharField(max_length=255, default="", blank=True)
    barangay = models.CharField(max_length=255, default="", blank=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName", "lastName"]

    objects = UserProfileManager()

    def __str__(self):
        return self.email

class Facility(models.Model):
    name = models.CharField(max_length=32)
    latitude = models.DecimalField(null=True, decimal_places=14,max_digits=17)
    longitude = models.DecimalField(null=True, decimal_places=14,max_digits=17)
    class Meta:
        verbose_name_plural = "Facilities"

class Message(models.Model):
    text = models.TextField(blank=True, null=True)
    user = models.OneToOneField(UserProfile, null=True, default=None, on_delete=models.CASCADE)
    sent_by = models.IntegerField(default=0)
    #sent_by = models.BooleanField(default=False,null=False)
    date_sent = models.DateField(default=datetime.now)
    



