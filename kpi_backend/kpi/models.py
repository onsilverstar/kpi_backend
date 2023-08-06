from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator
# from ..store.models import Address, OrderItem
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
# Create your models here.

class UserManager(BaseUserManager):
# standard for creating all types of users
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please provide Email")
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using = self.db)
                return user
        except:
            raise
    # create normal user method
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    # create superuser
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)

# Abstract class implementing feature model for admin compliant permisions
class User(AbstractBaseUser, PermissionsMixin, models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    title = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
    
class KPI_Metric(models.Model):
    guid = models.CharField(primary_key= True, max_length=40)
    name = models.CharField(max_length=20)
    target_quantitative = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=200)
    Created_At = models.DateTimeField()
    Updated_At = models.DateTimeField()

class Reporting_Lead(models.Model):
    user = models.ManyToManyField(User, default=None)
    title = "Reporting Lead"

class Manager(models.Model):
    user = models.ManyToManyField(User, default=None)
    title = "Manager"

class Senior_Manager(models.Model):
    user = models.ManyToManyField(User, default=None)
    title = "Senior_Manager"

class External(models.Model):
    user = models.ManyToManyField(User, default=None)
    title = "External"

class Director(models.Model):
    user = models.ManyToManyField(User, default=None)
    title = "Director"

class KPI_Measure(models.Model):
    guid = models.CharField(primary_key= True, max_length=40)
    KPI = models.ForeignKey(KPI_Metric, on_delete=models.CASCADE, default= None)
    operating_period = models.IntegerField()
    reporting_lead = models.ForeignKey(Reporting_Lead, default=None, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, default= None, on_delete=models.CASCADE)
    senior_manager = models.ForeignKey(Senior_Manager, default=None, on_delete=models.CASCADE)
    external_supervisor = models.ForeignKey(External, default=None, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, default=None, on_delete=models.CASCADE)
    stage = models.CharField(max_length=40)
    cycle_target_quantitative = models.DecimalField(decimal_places=2, max_digits=10, default=None)
    ytd_quantitative = models.DecimalField(decimal_places=2, max_digits=10, default=None)
    BRAG_status = models.BooleanField(default=False)
    comments = models.CharField(max_length=400)
    reporting_lead_approve = models.BooleanField(default=False)
    manager_approve = models.BooleanField(default=False)
    senior_manager_approve = models.BooleanField(default=False)
    external_supervisor_approve = models.BooleanField(default=False)
    director_approve = models.BooleanField(default=False)
    Created_At = models.DateTimeField()
    Updated_At = models.DateTimeField()

