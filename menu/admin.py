from django.contrib import admin
from .models import ConfigurationPaiement, Deposit, Utilisateur, Vehicule, Course, Paiement, Evaluation, Position, Notification, Tarification, Wallet

# =========================
# UTILISATEUR
# =========================
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(BaseUserAdmin):
    list_display = ('id','avatar_preview','username', 'get_full_name', 'email', 'telephone', 'type_utilisateur', 'statut', 'date_inscription')
    list_filter = ('type_utilisateur', 'statut')
    search_fields = ('username', 'email', 'telephone', 'first_name', 'last_name')
    readonly_fields = ('date_inscription', 'avatar_preview')
    ordering = ('-date_inscription',)

    # Ici tu conserves les champs de base de UserAdmin pour gérer correctement le mot de passe
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'telephone', 'avatar_preview')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Dates importantes', {'fields': ('last_login','date_inscription')}),
    )



# =========================
# VEHICULE
# =========================
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('id','marque', 'modele', 'plaque', 'type_vehicule', 'confort', 'chauffeur', 'capacite', 'statut','latitude','longitude', 'date_ajout')
    list_filter = ('type_vehicule', 'confort', 'statut')
    search_fields = ('marque', 'modele', 'plaque', 'chauffeur__username')
    readonly_fields = ('date_ajout',)
    ordering = ('-date_ajout',)


# =========================
# COURSE
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'passager', 'chauffeur', 'statut', 'prix_estime', 'date_creation')
    list_filter = ('statut', 'date_creation')
    search_fields = ('passager__username', 'chauffeur__username')


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
    
@admin.register(ConfigurationPaiement)
class ConfigurationPaiementAdmin(admin.ModelAdmin):
    list_display = ('pourcentage_chauffeur', 'pourcentage_admin', 'date_modification')
    readonly_fields = ('date_modification',)
    def has_add_permission(self, request):
        if ConfigurationPaiement.objects.exists():
            return False
        return True
    
    
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'admin_amount_cdf', 'admin_amount_usd',
        'driver_amount_cdf', 'driver_amount_usd',
        'date_modification'
    )
    search_fields = ('user__username',)
    readonly_fields = ('date_modification',)

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('chauffeur', 'amount_cdf', 'amount_usd', 'date_modification')
    search_fields = ('chauffeur__username',)
    readonly_fields = ('date_modification',)
    
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('passager', 'chauffeur', 'course', 'note', 'date_evaluation')
    search_fields = ('passager__username', 'chauffeur__username', 'course__id')
    list_filter = ('note',)