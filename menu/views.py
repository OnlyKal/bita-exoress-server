
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate

from menu.models import ConfigurationPaiement, Course, Deposit, Evaluation, Paiement, Tarification, Utilisateur, Vehicule, Wallet
from .serializers import ConfigurationPaiementSerializer, CourseSerializer, DepositSerializer, DevenirChauffeurSerializer, EvaluationSerializer, PaiementSerializer, UploadAvatarSerializer, UtilisateurSerializer, VehiculeSerializer, WalletSerializer  
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
        
class DevenirChauffeurView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        nouveau_type = request.data.get("type_utilisateur")
      # Mettre à jour le type d'utilisateur
        user.type_utilisateur = nouveau_type
        user.save()
        return Response({
            "status": True,
            "message": f"Votre profil a été mis à jour en tant que {nouveau_type}.",
            "data": UtilisateurSerializer(user).data
        }, status=status.HTTP_200_OK)

class DevenirChauffeurView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        serializer = DevenirChauffeurSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Votre profil a été mis à jour en tant que chauffeur.",
                "data": UtilisateurSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "message": "Erreur de validation.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
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
    
class AddVehiculeView(generics.CreateAPIView):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        chauffeur = request.user

        # 🔍 Vérifier si ce chauffeur a déjà un véhicule
        if Vehicule.objects.filter(chauffeur=chauffeur).exists():
            return Response({
                "status": False,
                "message": "Vous avez déjà un véhicule enregistré. Un seul véhicule est autorisé par chauffeur."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Si aucun véhicule n’est associé, on en crée un nouveau
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chauffeur=chauffeur)

        return Response({
            "status": True,
            "message": "Véhicule ajouté avec succès.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
        
    
class VehiculeListView(generics.ListAPIView):
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Vehicule.objects.all().order_by('-date_ajout')

class VehiculeDetailView(generics.ListAPIView):
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Vehicule.objects.filter(chauffeur=self.request.user)

class VehiculeUpdateView(generics.UpdateAPIView):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class VehiculeDeleteView(generics.DestroyAPIView):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    

# ========================= COURSE VIEWS =========================



# ✅ 1. Le passager crée une course
class CreateCourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(passager=self.request.user)


# ✅ 2. Le chauffeur voit les courses en attente
class PendingCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(statut='en_attente')


# ✅ 3. Le chauffeur accepte une course
class AcceptCourseView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        if course.statut != 'en_attente':
            return Response({"detail": "Course déjà acceptée ou terminée."}, status=status.HTTP_400_BAD_REQUEST)

        vehicule = Vehicule.objects.filter(chauffeur=request.user).first()
        if not vehicule:
            return Response({"detail": "Aucun véhicule enregistré pour ce chauffeur."}, status=status.HTTP_400_BAD_REQUEST)

        course.chauffeur = request.user
        course.vehicule = vehicule
        course.statut = 'acceptee'
        course.date_acceptation = timezone.now()
        course.save()

        return Response(CourseSerializer(course).data, status=status.HTTP_200_OK)


# ✅ 4. Liste des courses du chauffeur
class ChauffeurCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(chauffeur=self.request.user).order_by('-date_creation')


# ✅ 5. Liste des courses du passager
class PassagerCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(passager=self.request.user).order_by('-date_creation')
    



class PrixCourseAPIView(APIView):
    permission_classes = [AllowAny]  # Pas besoin d'auth pour estimation

    def post(self, request, *args, **kwargs):
        
        data = request.data
        type_vehicule = data.get('type_vehicule')
        confort = data.get('confort')
        distance_km = data.get('distance_km')
        duree_min = data.get('duree_min')

        if None in [type_vehicule, confort, distance_km, duree_min]:
            return Response(
                {"detail": "Tous les champs (type_vehicule, confort, distance_km, duree_min) sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            tarif = Tarification.objects.get(type_vehicule=type_vehicule, confort=confort)
        except Tarification.DoesNotExist:
            return Response({"detail": "Tarification non trouvée pour ce type et confort."}, status=status.HTTP_404_NOT_FOUND)

        prix = tarif.calcul_prix_dollars(distance_km=float(distance_km), duree_min=float(duree_min))

        return Response(prix, status=status.HTTP_200_OK)


# 🔹 Création d'une course par un passager
class CreateCourseView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(passager=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": True,
            "message": "Course créée avec succès. En attente d’un chauffeur.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# 🔹 Acceptation d’une course par un chauffeur
class AcceptCourseView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        chauffeur = request.user

        # Vérifier que la course est disponible
        if course.statut != 'en_attente':
            return Response({"detail": "Cette course n'est plus disponible."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Vérifier que le chauffeur a un véhicule
        vehicule = Vehicule.objects.filter(chauffeur=chauffeur).first()
        if not vehicule:
            return Response({"detail": "Aucun véhicule associé à ce chauffeur."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Mise à jour de la course
        course.statut = 'acceptee'
        course.chauffeur = chauffeur
        course.vehicule = vehicule
        # course.date_acceptation = timezone.now()
        course.save()

        serializer = self.get_serializer(course)
        return Response({
            "status": True,
            "message": "Course acceptée avec succès.",
            "data": serializer.data
        })


# 🔹 Annulation d’une course par le passager ou chauffeur
class CancelCourseView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user

        # Vérifier que la course n’est pas déjà terminée ou annulée
        if course.statut in ['terminee', 'annulee']:
            return Response({"detail": "Impossible d’annuler une course terminée ou déjà annulée."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si c’est bien le passager ou chauffeur concerné
        if course.passager != user and course.chauffeur != user:
            return Response({"detail": "Vous n’êtes pas autorisé à annuler cette course."},
                            status=status.HTTP_403_FORBIDDEN)

        # Mise à jour
        course.statut = 'annulee'
        course.save()

        serializer = self.get_serializer(course)
        return Response({
            "status": True,
            "message": "Course annulée avec succès.",
            "data": serializer.data
        })

# 🔹 Terminer une course par un chauffeur
class TerminerCourseView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        chauffeur = request.user

        # Vérifier que c'est bien le chauffeur concerné
        if course.chauffeur != chauffeur:
            return Response(
                {"detail": "Vous n'êtes pas autorisé à terminer cette course."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Vérifier que la course est en cours ou acceptée
        if course.statut not in ['acceptee', 'en_cours']:
            return Response(
                {"detail": "Impossible de terminer une course qui n'est pas en cours ou acceptée."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mettre à jour le statut et la date de fin
        course.statut = 'terminee'
        course.save()

        serializer = self.get_serializer(course)
        return Response({
            "status": True,
            "message": "Course terminée avec succès.",
            "data": serializer.data
        })

class MesCoursesPassagerView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(passager=self.request.user).order_by('-date_creation')

class CoursesDisponiblesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(statut='en_attente').order_by('-date_creation')

class MesCoursesChauffeurView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(chauffeur=self.request.user, statut__in=['acceptee', 'en_cours']).order_by('-date_creation')
    
class MesCoursesChauffeurViewTerminee(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(chauffeur=self.request.user, statut__in=['terminee']).order_by('-date_creation')
    

class AddPaiementView(generics.CreateAPIView):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user = request.user
        try:
            course = Course.objects.get(id=data.get('course'))
        except Course.DoesNotExist:
            return Response({"detail": "Course introuvable."}, status=status.HTTP_404_NOT_FOUND)
        if Paiement.objects.filter(course=course, statut='réussi').exists():
            return Response({"detail": "Un paiement réussi existe déjà pour cette course."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        paiement = serializer.save()
        return Response({
            "status": True,
            "message": "Paiement enregistré avec succès.",
            "data": PaiementSerializer(paiement).data
        }, status=status.HTTP_201_CREATED)
        
    
class MesPaiementsView(generics.ListAPIView):
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Paiement.objects.filter(course__passager=user).order_by('-date_paiement')

class ConfigurationPaiementView(generics.RetrieveAPIView):
    serializer_class = ConfigurationPaiementSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
 
        config, _ = ConfigurationPaiement.objects.get_or_create(
            id=1,
            defaults={
                'pourcentage_chauffeur': 10.00,
                'pourcentage_admin': 90.00
            }
        )
        return config
    


# 🔹 Initialiser / Ajouter un montant
class AddAmountWalletView(generics.GenericAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

        amount = float(data.get("amount", 0))
        devise = data.get("devise", "CDF").lower()
        is_admin = data.get("is_admin", False)

        wallet, _ = Wallet.objects.get_or_create(user=user)
        wallet.add_amount(amount, devise, is_admin)

        return Response({
            "status": True,
            "message": f"Montant ajouté avec succès ({amount} {devise.upper()})",
            "data": WalletSerializer(wallet).data
        })
        

# 🔹 Get wallet for admin
class GetWalletForAdminView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        return wallet


# 🔹 Get wallet for driver
class GetWalletForDriverView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        return wallet


# 🔹 Retrait (withdraw cash)
class WithdrawWalletView(generics.GenericAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

        amount = float(data.get("amount", 0))
        devise = data.get("devise", "CDF").lower()
        is_admin = data.get("is_admin", False)

        wallet, _ = Wallet.objects.get_or_create(user=user)
        wallet.withdraw_cash(amount, devise, is_admin)

        return Response({
            "status": True,
            "message": f"Retrait de {amount} {devise.upper()} effectué avec succès.",
            "data": WalletSerializer(wallet).data
        })


# 🔹 Transfert interne admin <-> driver
class TransfertWalletView(generics.GenericAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        sender = request.user
        receiver_id = data.get("receiver_id")
        amount = float(data.get("amount", 0))
        devise = data.get("devise", "CDF").lower()

        try:
            receiver = Utilisateur.objects.get(id=receiver_id)
        except Utilisateur.DoesNotExist:
            return Response({"detail": "Destinataire introuvable."}, status=status.HTTP_404_NOT_FOUND)

        sender_wallet, _ = Wallet.objects.get_or_create(user=sender)
        receiver_wallet, _ = Wallet.objects.get_or_create(user=receiver)

        # Vérification du solde
        if devise == "cdf" and sender_wallet.driver_amount_cdf < amount:
            return Response({"detail": "Solde insuffisant."}, status=status.HTTP_400_BAD_REQUEST)
        if devise == "usd" and sender_wallet.driver_amount_usd < amount:
            return Response({"detail": "Solde insuffisant."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrait et ajout
        sender_wallet.withdraw_cash(amount, devise, is_admin=False)
        receiver_wallet.add_amount(amount, devise, is_admin=False)

        return Response({
            "status": True,
            "message": f"Transfert de {amount} {devise.upper()} effectué avec succès.",
            "sender": WalletSerializer(sender_wallet).data,
            "receiver": WalletSerializer(receiver_wallet).data
        })
from django.db.models import Sum     
class GetTotalAdminWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_cdf = Wallet.objects.aggregate(total=Sum('admin_amount_cdf'))['total'] or 0
        total_usd = Wallet.objects.aggregate(total=Sum('admin_amount_usd'))['total'] or 0

        return Response({
            "status": True,
            "message": "Total global du portefeuille admin.",
            "total_admin_cdf": round(total_cdf, 2),
            "total_admin_usd": round(total_usd, 2),
        })
        

# ➕ Ajouter un dépôt
class AddDepositView(generics.GenericAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        amount = float(data.get("amount", 0))
        devise = data.get("devise", "CDF").lower()

        deposit, _ = Deposit.objects.get_or_create(chauffeur=request.user)
        deposit.add_amount(amount, devise)

        return Response({
            "status": True,
            "message": f"Montant ajouté au dépôt ({amount} {devise.upper()})",
            "data": DepositSerializer(deposit).data
        })

# ➖ Retirer du dépôt
class WithdrawDepositView(generics.GenericAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        amount = float(data.get("amount", 0))
        devise = data.get("devise", "CDF").lower()

        deposit, _ = Deposit.objects.get_or_create(chauffeur=request.user)
        try:
            deposit.withdraw_amount(amount, devise)
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": f"Montant retiré du dépôt ({amount} {devise.upper()})",
            "data": DepositSerializer(deposit).data
        })

# 🔎 Récupérer le dépôt
class GetDepositView(generics.RetrieveAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        deposit, _ = Deposit.objects.get_or_create(chauffeur=self.request.user)
        return deposit
    
# 🔹 Créer une évaluation
class AddEvaluationView(generics.CreateAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(passager=self.request.user)

# 🔹 Liste des évaluations d’un chauffeur
class EvaluationsChauffeurView(generics.ListAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chauffeur_id = self.kwargs.get('chauffeur_id')
        return Evaluation.objects.filter(chauffeur_id=chauffeur_id).order_by('-date_evaluation')

# 🔹 Liste des évaluations données par un passager
class EvaluationsPassagerView(generics.ListAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Evaluation.objects.filter(passager=self.request.user).order_by('-date_evaluation')