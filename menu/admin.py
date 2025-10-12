from django.contrib import admin
from .models import Utilisateur, Vehicule, Course, Paiement, Evaluation, Position, Notification, Tarification

# =========================
# UTILISATEUR
# =========================
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('avatar_preview','username', 'get_full_name', 'email', 'telephone', 'type_utilisateur', 'statut', 'date_inscription')
    list_filter = ('type_utilisateur', 'statut')
    search_fields = ('username', 'email', 'telephone', 'first_name', 'last_name')
    readonly_fields = ('date_inscription', 'avatar_preview')
    ordering = ('-date_inscription',)


# =========================
# VEHICULE
# =========================
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'plaque', 'type_vehicule', 'confort', 'chauffeur', 'capacite', 'statut', 'date_ajout')
    list_filter = ('type_vehicule', 'confort', 'statut')
    search_fields = ('marque', 'modele', 'plaque', 'chauffeur__username')
    readonly_fields = ('date_ajout',)
    ordering = ('-date_ajout',)


# =========================
# COURSE
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'passager', 'chauffeur', 'point_depart', 'point_arrivee', 'distance_km', 'duree_min', 'prix', 'statut_course', 'mode_paiement', 'date_creation')
    list_filter = ('statut_course', 'mode_paiement')
    search_fields = ('passager__username', 'chauffeur__username', 'point_depart', 'point_arrivee')
    readonly_fields = ('date_creation', 'date_fin')
    ordering = ('-date_creation',)


# =========================
# PAIEMENT
# =========================
@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'montant', 'moyen', 'devise', 'statut', 'date_paiement')
    list_filter = ('statut', 'moyen')
    search_fields = ('course__passager__username', 'course__chauffeur__username')
    readonly_fields = ('date_paiement',)
    ordering = ('-date_paiement',)


# =========================
# EVALUATION
# =========================
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'auteur', 'cible', 'course', 'note', 'date_evaluation')
    list_filter = ('note',)
    search_fields = ('auteur__username', 'cible__username', 'course__id')
    readonly_fields = ('date_evaluation',)
    ordering = ('-date_evaluation',)


# =========================
# POSITION
# =========================
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('chauffeur', 'latitude', 'longitude', 'derniere_mise_a_jour')
    search_fields = ('chauffeur__username',)
    readonly_fields = ('derniere_mise_a_jour',)
    ordering = ('-derniere_mise_a_jour',)


# =========================
# NOTIFICATION
# =========================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'titre', 'statut', 'date_envoi')
    list_filter = ('statut',)
    search_fields = ('utilisateur__username', 'titre', 'message')
    readonly_fields = ('date_envoi',)
    ordering = ('-date_envoi',)


# =========================
# TARIFICATION
# =========================
@admin.register(Tarification)
class TarificationAdmin(admin.ModelAdmin):
    list_display = ('type_vehicule', 'confort', 'tarif_km', 'tarif_min', 'supplement', 'promo', 'taux', 'date_creation')
    list_filter = ('type_vehicule', 'confort')
    search_fields = ('type_vehicule', 'confort')
    readonly_fields = ('date_creation', 'date_modification')
    ordering = ('-date_creation',)
