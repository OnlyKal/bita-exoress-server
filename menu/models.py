from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

from server import settings

# =========================
# UTILISATEUR
# =========================
class Utilisateur(AbstractUser):
    TYPE_UTILISATEUR = [
        ('passager', 'Passager'),
        ('chauffeur', 'Chauffeur'),
        ('admin', 'Administrateur'),
    ]
    STATUT_CHOIX = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('supprimé', 'Supprimé'),
    ]
    
  
    telephone = models.CharField(max_length=30, unique=False)
    email = models.EmailField(max_length=150, unique=False)
    type_utilisateur = models.CharField(max_length=20, choices=TYPE_UTILISATEUR, default='passager')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    permis = models.ImageField(upload_to='permis/', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='actif')
    date_inscription = models.DateTimeField(auto_now_add=True)

    def avatar_preview(self):
        if self.avatar:
            return mark_safe(f'<div style="width:50px;height:50px;border:1px solid #000;border-radius:10px;background-image:url({self.avatar.url});background-size:cover;background-position:center;"></div>')
        return "No Image"
    avatar_preview.short_description = 'Avatar'
    def __str__(self):
        return self.get_full_name() or self.username


# =========================
# VEHICULE
# =========================


class Vehicule(models.Model):
    TYPE_VEHICULE = [
        ('moto', 'Moto'),
        ('voiture', 'Voiture'),
        ('van', 'Van'),
        ('bus', 'Bus'),
    ]

    CONFORT_CHOIX = [
        ('standard', 'Standard'),
        ('confort', 'Confort'),
        ('vip', 'VIP'),
    ]

    STATUT_VEHICULE = [
        ('actif', 'Actif'),
        ('en_maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
        ('réservé', 'Réservé'),
    ]

    chauffeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicules'
    )
    confort = models.CharField(max_length=20,null=True, blank=True, choices=CONFORT_CHOIX, default='standard')
    marque = models.CharField(max_length=100,null=True, blank=True,)
    modele = models.CharField(max_length=100,null=True, blank=True,)
    plaque = models.CharField(max_length=50, unique=True,null=True, blank=True,)
    couleur = models.CharField(max_length=50,null=True, blank=True,)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE, default='voiture',null=True, blank=True,)
    capacite = models.IntegerField(default=4,null=True, blank=True,)
    statut = models.CharField(max_length=20,null=True, blank=True, choices=STATUT_VEHICULE, default='actif')

    # 📍 Localisation GPS
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude actuelle du véhicule")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude actuelle du véhicule")

  

    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.plaque}"


# =========================
# COURSE
# =========================
class Course(models.Model):
    STATUT_COURSE = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    passager = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='courses_passager'
    )
    chauffeur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        related_name='courses_chauffeur',
        null=True, blank=True
    )
    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    depart_latitude = models.FloatField(null=True, blank=True, default=0.000)
    depart_longitude = models.FloatField(null=True, blank=True, default=0.000)
    destination_latitude = models.FloatField(null=True, blank=True, default=0.000)
    destination_longitude = models.FloatField(null=True, blank=True , default=0.000)

    distance = models.FloatField(null=True, blank=True)  # en mètres
    duree_estimee = models.FloatField(null=True, blank=True)  # en secondes
    prix_estime = models.FloatField(null=True, blank=True)

    statut = models.CharField(max_length=20, choices=STATUT_COURSE, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_acceptation = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Course #{self.id} - {self.passager.username} ({self.statut})"


# =========================
# PAIEMENT
# =========================

class Paiement(models.Model):
    STATUT_PAIEMENT = [
        ('réussi', 'Réussi'),
        ('échoué', 'Échoué'),
        ('en_attente', 'En attente'),
    ]
    MOYEN = [
        ('espèces', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('mobile_money', 'Mobile Money'),
    ]
    DEVISE = [
        ('cdf', 'CDF'),
        ('usd', 'USD'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='paiements')
    devise = models.CharField(max_length=10, choices=DEVISE, default='CDF')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    moyen = models.CharField(max_length=20, choices=MOYEN, default='espèces')
    statut = models.CharField(max_length=20, choices=STATUT_PAIEMENT, default='en_attente')
    date_paiement = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Paiement {self.id} - {self.montant} {self.moyen}"


# =========================
# EVALUATION
# =========================
class Evaluation(models.Model):
    passager = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evaluations_donnees')
    chauffeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evaluations_recues')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='evaluations')
    note = models.IntegerField()  # note sur 5
    commentaire = models.TextField(null=True, blank=True)
    date_evaluation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_evaluation']

    def __str__(self):
        return f"Note {self.note}/5 par {self.passager.username} pour {self.chauffeur.username}"


# =========================
# POSITION
# =========================
class Position(models.Model):
    chauffeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='positions')
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    derniere_mise_a_jour = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.chauffeur} - ({self.latitude}, {self.longitude})"


# =========================
# NOTIFICATION
# =========================
class Notification(models.Model):
    STATUT_NOTIF = [
        ('non_lu', 'Non lu'),
        ('lu', 'Lu'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=150)
    message = models.TextField()
    statut = models.CharField(max_length=10, choices=STATUT_NOTIF, default='non_lu')
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif à {self.utilisateur}: {self.titre}"


# =========================
# TARIFICATION
# =========================
class Tarification(models.Model):
    TYPE_VEHICULE = [
        ('moto', 'Moto'),
        ('voiture', 'Voiture'),
        ('van', 'Van'),
        ('bus', 'Bus'),
    ]
    CONFORT_CHOIX = [
        ('standard', 'Standard'),
        ('confort', 'Confort'),
        ('vip', 'VIP'),
    ]

    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE, default='voiture')
    confort = models.CharField(max_length=20, choices=CONFORT_CHOIX, default='standard')
    tarif_km = models.FloatField(  default=1)
    tarif_min = models.FloatField(  default=1)
    supplement = models.FloatField(  default=0)
    promo = models.FloatField(default=0)
    taux = models.IntegerField(default=2000)  # taux de conversion pour prix en francs
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.type_vehicule} - {self.confort} | {self.tarif_km} CDF/km"

    def calcul_prix(self, distance_km, duree_min):
        """
        Calcul du prix final en francs, après application du taux et promo.
        """
        prix_base = (self.tarif_km * distance_km) + (self.tarif_min * duree_min) + self.supplement
        prix_taux = prix_base * self.taux
        prix_final = prix_taux * (1 - (self.promo / 100))
        return round(prix_final, 2)

    def calcul_prix_dollars(self, distance_km, duree_min, taux_change_usd=0.00051):
        """
        Retourne un dictionnaire avec prix en francs et équivalent dollars.
        taux_change_usd = 1 CDF -> USD (modifiable selon le cours actuel)
        """
        prix_cdf = self.calcul_prix(distance_km, duree_min)
        prix_usd = round(prix_cdf * taux_change_usd, 2)
        return {
            "prix_cdf": prix_cdf,
            "prix_usd": prix_usd
        }


class ConfigurationPaiement(models.Model):
    pourcentage_chauffeur = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)
    pourcentage_admin = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration Paiement"
        verbose_name_plural = "Configuration Paiements"

    def save(self, *args, **kwargs):
        # Assurer qu'un seul enregistrement existe
        if not self.pk and ConfigurationPaiement.objects.exists():
            raise ValueError("Une seule configuration est autorisée.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Config Paiement (Admin: {self.pourcentage_admin}%, Chauffeur: {self.pourcentage_chauffeur}%)"


class Wallet(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="wallet")

    admin_amount_cdf = models.FloatField(default=0)
    admin_amount_usd = models.FloatField(default=0)
    driver_amount_cdf = models.FloatField(default=0)
    driver_amount_usd = models.FloatField(default=0)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet de {self.user.username}"
    def add_amount(self, amount, devise, is_admin=False):
        """Ajoute un montant selon le type d’utilisateur et la devise"""
        if devise.lower() == 'cdf':
            if is_admin:
                self.admin_amount_cdf += amount
            else:
                self.driver_amount_cdf += amount
        elif devise.lower() == 'usd':
            if is_admin:
                self.admin_amount_usd += amount
            else:
                self.driver_amount_usd += amount
        self.save()

    def withdraw_cash(self, amount, devise, is_admin=False):
        """Retire un montant du portefeuille"""
        if devise.lower() == 'cdf':
            if is_admin:
                if self.admin_amount_cdf >= amount:
                    self.admin_amount_cdf -= amount
            else:
                if self.driver_amount_cdf >= amount:
                    self.driver_amount_cdf -= amount
        elif devise.lower() == 'usd':
            if is_admin:
                if self.admin_amount_usd >= amount:
                    self.admin_amount_usd -= amount
            else:
                if self.driver_amount_usd >= amount:
                    self.driver_amount_usd -= amount
        self.save()


class Deposit(models.Model):
    chauffeur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deposit")
    amount_cdf = models.FloatField( default=0)
    amount_usd = models.FloatField( default=0)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Depot de {self.chauffeur.username}"
    def add_amount(self, amount, devise):
        if devise.lower() == 'cdf':
            self.amount_cdf += amount
        elif devise.lower() == 'usd':
            self.amount_usd += amount
        self.save()
    def withdraw_amount(self, amount, devise):
        if devise.lower() == 'cdf' and self.amount_cdf >= amount:
            self.amount_cdf -= amount
        elif devise.lower() == 'usd' and self.amount_usd >= amount:
            self.amount_usd -= amount
        else:
            raise ValueError("Solde insuffisant")
        self.save()