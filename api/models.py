from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    code_conducteur = models.CharField(max_length=255)
    nom_complet = models.CharField(max_length=255)
    date_naiss = models.DateField(null=True, blank=True)
    ville = models.CharField(max_length=255)
    num_permi = models.CharField(max_length=255)
    num_cni = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_complet', 'code_conducteur']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateurs',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateurs',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.nom_complet

class Voiture(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, related_name='voitures', on_delete=models.CASCADE)
    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    annee = models.IntegerField()
    immatriculation = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"

class Accident(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, related_name='accidents', on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, related_name='accidents', on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Accident {self.id} - {self.utilisateur.nom_complet} - {self.voiture.immatriculation} - {self.date}"

