from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Utiliser UserAdmin pour s'assurer que le modèle CustomUser est géré comme un modèle d'utilisateur
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Vous pouvez personnaliser l'affichage des champs ici si vous le souhaitez
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
