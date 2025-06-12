from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class RoleChoices(models.TextChoices):

    ADMIN = 'Admin', 'Admin'

    USER = 'User', 'User'

class Profile(AbstractUser):

    role = models.CharField(max_length=10,choices=RoleChoices.choices)

    def __str__(self):

        return self.email
    
    class Meta:

        verbose_name = 'Profile'

        verbose_name_plural = 'Profiles'

        ordering = ['email'] 