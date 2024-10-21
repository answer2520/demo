from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)

    # Modifiez les relations pour éviter le conflit
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Nom unique pour éviter le conflit
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Nom unique pour éviter le conflit
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
