from rest_framework import serializers

from menu.func import Base64ImageFunc
from .models import ConfigurationPaiement, Deposit, Utilisateur, Vehicule, Course, Paiement, Evaluation, Position, Notification, Tarification, Wallet

# =========================
# UTILISATEUR
# =========================

class UtilisateurSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'telephone',
            'type_utilisateur', 'statut', 'date_inscription', 'avatar_url','permis'
        ]
        
        extra_kwargs = {
            'email': {'validators': []},
            'telephone': {'validators': []},
        }
        
    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None



class UploadAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageFunc()
    class Meta:
        model = Utilisateur
        fields = ["avatar"]
    def create(self, validated_data):
        user = self.context.get("avatar")
        return Utilisateur.objects.create(user=user, **validated_data)
    
class DevenirChauffeurSerializer(serializers.ModelSerializer):
    permis = Base64ImageFunc()
    class Meta:
        model = Utilisateur
        fields = ["permis"]

    def update(self, instance, validated_data):
        instance.permis = validated_data.get("permis", instance.permis)
        instance.type_utilisateur = "chauffeur"
        instance.save()
        return instance
# =========================
# VEHICULE
# =========================
class VehiculeSerializer(serializers.ModelSerializer):
    chauffeur = UtilisateurSerializer(read_only=True)

    class Meta:
        model = Vehicule
        fields = [
            'id', 'chauffeur', 'marque', 'modele', 'plaque', 'couleur','latitude','longitude',
            'type_vehicule', 'confort', 'capacite', 'statut', 'date_ajout'
        ]


# =========================
# COURSE
# =========================

class CourseSerializer(serializers.ModelSerializer):
    passager_name = serializers.SerializerMethodField()
    chauffeur_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = [
            'statut',
            'chauffeur',
            'vehicule',
            'date_creation',
            'date_acceptation',
            'date_fin'
        ]

    def get_passager_name(self, obj):
        """Retourne le nom complet du passager s’il existe, sinon le username"""
        if obj.passager:
            full_name = f"{obj.passager.first_name} {obj.passager.last_name}".strip()
            return full_name or obj.passager.username
        return None

    def get_chauffeur_name(self, obj):
        """Retourne le nom complet du chauffeur s’il existe, sinon le username"""
        if obj.chauffeur:
            full_name = f"{obj.chauffeur.first_name} {obj.chauffeur.last_name}".strip()
            return full_name or obj.chauffeur.username
        return None

# =========================
# PAIEMENT
# =========================
class PaiementSerializer(serializers.ModelSerializer):
    course_info = serializers.SerializerMethodField()

    class Meta:
        model = Paiement
        fields = '__all__'
        read_only_fields = ['statut', 'date_paiement']

    def get_course_info(self, obj):
        return {
            "id": obj.course.id,
            "passager": obj.course.passager.username,
            "chauffeur": obj.course.chauffeur.username if obj.course.chauffeur else None,
            "prix_estime": obj.course.prix_estime,
        }



# =========================
# POSITION
# =========================
class PositionSerializer(serializers.ModelSerializer):
    chauffeur = UtilisateurSerializer(read_only=True)

    class Meta:
        model = Position
        fields = [
            'id', 'chauffeur', 'latitude', 'longitude', 'derniere_mise_a_jour'
        ]


# =========================
# NOTIFICATION
# =========================
class NotificationSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'utilisateur', 'titre', 'message', 'statut', 'date_envoi'
        ]


# =========================
# TARIFICATION
# =========================

class TarificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarification
        fields = '__all__'
        read_only_fields = ['date_creation', 'date_modification']

class ConfigurationPaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationPaiement
        fields = '__all__'
        
class WalletSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'
        
class DepositSerializer(serializers.ModelSerializer):
    chauffeur_name = serializers.CharField(source='chauffeur.username', read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'
        
        
        
class EvaluationSerializer(serializers.ModelSerializer):
    passager_name = serializers.CharField(source='passager.username', read_only=True)
    chauffeur_name = serializers.CharField(source='chauffeur.username', read_only=True)
    course_id = serializers.IntegerField(source='course.id', read_only=True)

    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ['passager', 'date_evaluation']