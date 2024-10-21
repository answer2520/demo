from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.signing import Signer, BadSignature  
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model 

signer = Signer()

# API d'inscription (signup)
@api_view(['POST'])
def signup(request):
    # Récupérer les données de la requête
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    User = get_user_model()  # Obtenez le modèle d'utilisateur personnalisé

    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Cet utilisateur existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)

    # Créer un nouvel utilisateur
    user = User.objects.create(
        username=username,
        password=make_password(password),
        email=email,
        is_active=False  # Désactiver jusqu'à la vérification de l'email
    )
    send_verification_email(user)

    return Response({'message': 'Utilisateur créé avec succès. Veuillez vérifier votre email'}, status=status.HTTP_201_CREATED)

# Fonction pour envoyer l'e-mail de vérification
def send_verification_email(user):
    token = signer.sign(user.email)
    verification_link = f"http://localhost:8000/api/verify-email/{token}"
    
    subject = 'Vérification de votre email'
    message = f'Cliquez sur le lien suivant pour vérifier votre email : {verification_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    
    send_mail(subject, message, from_email, [user.email])


# API pour vérifier l'email à partir du token
@api_view(['GET'])
def verify_email(request, token):
    User = get_user_model()

    try:
        email = signer.unsign(token)
        user = User.objects.get(email=email)
        
        if user.is_active:
            return Response({'message': 'Votre email est déjà vérifié.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Activer l'utilisateur
        user.is_active = True
        user.save()
        
        return Response({'message': 'Votre email a été vérifié avec succès. Vous pouvez maintenant vous connecter.'}, status=status.HTTP_200_OK)
    
    except (User.DoesNotExist, signer.BadSignature):
        return Response({'error': 'Le lien de vérification est invalide.'}, status=status.HTTP_400_BAD_REQUEST)


# Si tu as besoin d'une vue d'inscription pour des tests via HTML, sinon tu peux ignorer cette partie
def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']

        # Créer et enregistrer l'utilisateur
        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_active = False  # Désactiver l'utilisateur jusqu'à ce qu'il vérifie l'e-mail
        user.save()

        # Envoyer l'e-mail de vérification
        send_verification_email(user)

        return HttpResponse("Veuillez vérifier votre email pour activer votre compte.")

    return render(request, 'signup.html')
