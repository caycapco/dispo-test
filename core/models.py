from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, fullname, password):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, fullname, password):
        """ Create a new superuser profile """
        user = self.create_user(email,fullname, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = UserProfileManager()

    def __str__(self):
        return self.email