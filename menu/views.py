
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate

from menu.models import Utilisateur
from .serializers import UploadAvatarSerializer, UtilisateurSerializer  
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class SignInView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username:
            email = request.data.get("email")
            try:
                user_obj = Utilisateur.objects.get(email=email)
                username = user_obj.username
            except Utilisateur.DoesNotExist:
                return Response({"status": False, "message": "Email invalide"}, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(request, username=username, password=password)
        if user:
            token = get_tokens_for_user(user)
            return Response({
                "status": True,
                "message": "Connexion réussie",
                "token": "Bearer " + token,
                "data": UtilisateurSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({"status": False, "message": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
    
class SignupView(CreateAPIView):
    serializer_class = UtilisateurSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "status": True,
            "message": "Utilisateur créé avec succès",
            "token": "Bearer "+token,
            "data": UtilisateurSerializer(user).data
        }, status=status.HTTP_201_CREATED)
        
        
class UpdateUserInfoView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UtilisateurSerializer

    def get_object(self):
        return self.request.user
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": True,
            "message": "Informations mises à jour",
            "data": serializer.data
        })
        
        
class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not user.check_password(old_password):
            return Response({"status": False, "message": "Ancien mot de passe incorrect"}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({"status": True, "message": "Mot de passe mis à jour"})
    

class UploadAvatarView(generics.UpdateAPIView):
    serializer_class = UploadAvatarSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)