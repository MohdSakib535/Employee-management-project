from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True,related_name='users')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customUser_user_set',  # Add related_name argument
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions=models.ManyToManyField(
        'auth.Permission',
        related_name='customUser_user_set',  # Add related_name argument
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )	

	

    def __str__(self):
        return f'{self.username}'
    

