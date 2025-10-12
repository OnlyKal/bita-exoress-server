from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

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

    chauffeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='vehicules')
    confort = models.CharField(max_length=20, choices=CONFORT_CHOIX, default='standard')
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    plaque = models.CharField(max_length=50)
    couleur = models.CharField(max_length=50)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE, default='voiture')
    capacite = models.IntegerField(default=4)
    statut = models.CharField(max_length=20, choices=STATUT_VEHICULE, default='actif')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.plaque}"


# =========================
# COURSE
# =========================
class Course(models.Model):
    MODE_PAIEMENT = [
        ('espèces', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('mobile_money', 'Mobile Money'),
    ]
    STATUT_COURSE = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminée', 'Terminée'),
        ('annulée', 'Annulée'),
    ]

    passager = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='courses_passager')
    chauffeur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_chauffeur')
    point_depart = models.CharField(max_length=255)
    point_arrivee = models.CharField(max_length=255)
    distance_km = models.DecimalField(max_digits=8, decimal_places=2)
    duree_min = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT, default='espèces')
    statut_course = models.CharField(max_length=20, choices=STATUT_COURSE, default='en_attente')
    note_passager = models.IntegerField(null=True, blank=True)
    note_chauffeur = models.IntegerField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Course #{self.id} - {self.passager} vers {self.point_arrivee}"


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
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evaluations_donnees')
    cible = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evaluations_recues')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='evaluations')
    note = models.IntegerField()
    commentaire = models.TextField(null=True, blank=True)
    date_evaluation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note {self.note}/5 par {self.auteur} pour {self.cible}"


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
    tarif_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tarif_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promo = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    taux = models.IntegerField(default=1)
    date_creation = models.DateTimeField(auto_now_add=True)

    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type_vehicule} - {self.confort} | {self.tarif_km} CDF/km"

    def calcul_prix(self, distance_km, duree_min):
        prix_base = (self.tarif_km * distance_km) + (self.tarif_min * duree_min) + self.supplement
        prix_taux = prix_base * self.taux
        prix_final = prix_taux * (1 - (self.promo / 100))
        return round(prix_final, 2)
