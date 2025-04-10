from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Miqaat(models.Model):
    EVENT_TYPES = (
        ('general_miqaats', 'General Miqaats'),
        ('private_events', 'Private Events'),
        ('ramadan', 'Ramadan'),
    )
    
    miqaat_name = models.CharField(max_length=255)
    miqaat_date = models.DateField()
    hijri_date = models.CharField(max_length=50, blank=True, null=True)
    miqaat_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField(blank=True, null=True)

    thaals_polled = models.PositiveIntegerField(default=0)
    thaals_cooked = models.PositiveIntegerField(default=0)
    thaals_served = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.miqaat_name} - {self.miqaat_date}"

class Zone(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    its= models.CharField(max_length=8,unique=True)
    full_name = models.CharField(max_length=255)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='members')
    miqaat = models.ForeignKey(Miqaat, on_delete=models.CASCADE, related_name='members')
    counter = models.ForeignKey('Counter', on_delete=models.SET_NULL, null=True, related_name='members')
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    mohalla = models.TextField(blank=True, null=True)    

    def __str__(self):
        return f"{self.name} ({self.its})"

class Unit(models.Model):
    name = models.CharField(max_length=255)
   
    def __str__(self):
        return self.unit_name

class Container(models.Model):
    name = models.CharField(max_length=255)
   
    def __str__(self):
        return self.unit_name

class Counter(models.Model):
    name = models.CharField(max_length=255)
    zone= models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='counters')

    def __str__(self):
        return self.name
    
class MiqaatAttendance(models.Model):
    miqaat = models.ForeignKey(Miqaat, on_delete=models.CASCADE, related_name='attendances')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='attendances')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE,null=True, related_name='attendances')
    checkin_time = models.TimeField()
    checkout_time = models.TimeField()

    def __str__(self):
        return f"{self.member} - {self.miqaat}"

class MiqaatZone(models.Model):
    miqaat = models.ForeignKey(Miqaat, on_delete=models.CASCADE, related_name='miqaat_zones')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='miqaat_zones')

    def __str__(self):
        return f"{self.miqaat} - {self.zone}"


class MiqaatMenu(models.Model):
    miqaat = models.ForeignKey(Miqaat, on_delete=models.CASCADE, related_name='miqaat_menus')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='miqaat_menus')

    def __str__(self):
        return f"{self.miqaat} - {self.menu}"


class CounterPacking(models.Model):
    miqaat = models.ForeignKey(Miqaat, on_delete=models.CASCADE, related_name='counter_packings')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='counter_packings')
    miqaat_menu = models.ForeignKey(MiqaatMenu, on_delete=models.CASCADE, related_name='counter_packings')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='counter_packings')
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='counter_packings')
    quantity = models.PositiveIntegerField(default=0)
    filled_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.miqaat_menu} - {self.zone}"


class Distribution(models.Model):
    miqaat = models.ForeignKey(Miqaat, on_delete=models.CASCADE, related_name='distributions')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='distributions')
    counter_packing = models.ForeignKey(CounterPacking, on_delete=models.CASCADE, related_name='distributions')
    ibadullah_count = models.PositiveIntegerField(default=0)
    mumin_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.zone} - {self.miqaat}"


class LeftOverDegs(models.Model):
    miqaat = models.ForeignKey(Miqaat, on_delete=models.CASCADE, related_name='leftover_degs')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='leftover_degs')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='leftover_degs')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='leftover_degs')
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='leftover_degs')
    total_cooked = models.PositiveIntegerField(default=0)
    total_received = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.menu} - {self.zone}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
