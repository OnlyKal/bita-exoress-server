from rest_framework import serializers

from menu.func import Base64ImageFunc
from .models import Utilisateur, Vehicule, Course, Paiement, Evaluation, Position, Notification, Tarification

# =========================
# UTILISATEUR
# =========================
class UtilisateurSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'telephone',
            'type_utilisateur', 'statut', 'date_inscription', 'avatar_url'
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
# =========================
# VEHICULE
# =========================
class VehiculeSerializer(serializers.ModelSerializer):
    chauffeur = UtilisateurSerializer(read_only=True)

    class Meta:
        model = Vehicule
        fields = [
            'id', 'chauffeur', 'marque', 'modele', 'plaque', 'couleur',
            'type_vehicule', 'confort', 'capacite', 'statut', 'date_ajout'
        ]


# =========================
# COURSE
# =========================
class CourseSerializer(serializers.ModelSerializer):
    passager = UtilisateurSerializer(read_only=True)
    chauffeur = UtilisateurSerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'passager', 'chauffeur', 'point_depart', 'point_arrivee',
            'distance_km', 'duree_min', 'prix', 'mode_paiement', 'statut_course',
            'note_passager', 'note_chauffeur', 'date_creation', 'date_fin'
        ]


# =========================
# PAIEMENT
# =========================
class PaiementSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Paiement
        fields = [
            'id', 'course', 'montant', 'moyen', 'devise', 'statut', 'date_paiement'
        ]


# =========================
# EVALUATION
# =========================
class EvaluationSerializer(serializers.ModelSerializer):
    auteur = UtilisateurSerializer(read_only=True)
    cible = UtilisateurSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Evaluation
        fields = [
            'id', 'auteur', 'cible', 'course', 'note', 'commentaire', 'date_evaluation'
        ]


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
        fields = [
            'id', 'type_vehicule', 'confort', 'tarif_km', 'tarif_min',
            'supplement', 'promo', 'taux', 'date_creation', 'date_modification'
        ]



