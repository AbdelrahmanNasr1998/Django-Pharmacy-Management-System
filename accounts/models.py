from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator







# 1. creating Custome Manager for User Model
class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        # convert all in lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, username, password, **other_fields)

Account_Type = (
        ('pharmacy', 'Pharmacy'),
        ('hospital', 'Hospital'),
        ('school', 'School'),
        ('sales', 'Sales'),
)


# 2. Creating Custom User Model
class Accounts(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(_('email address'), max_length=32, unique=True)
    phone_number = models.CharField(max_length=24, blank=True, null=True)
    type = models.CharField(max_length=8, choices=Account_Type)
    start_date = models.DateTimeField(default=timezone.now)
    billing = models.IntegerField(default=0)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'

    # required for superuser
    REQUIRED_FIELDS = ['email', ]


    def __str__(self):
        return self.username


class Payments(models.Model):
    username = models.ForeignKey('accounts.Accounts', on_delete=models.CASCADE)
    start_billing = models.DateField(default=timezone.now)
    end_billing = models.DateField(default=timezone.now)
    ammount = models.IntegerField()

    class Meta:
        ordering = ("-start_billing","end_billing")