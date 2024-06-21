import os
import django
import random
from faker import Faker
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accident_detection.settings')
django.setup()

from api.models import Utilisateur, Voiture, Accident

fake = Faker()

def create_utilisateur():
    return Utilisateur.objects.create_user(
        email=fake.email(),
        password='password123',
        code_conducteur=fake.bothify(text='????-####'),
        nom_complet=fake.name(),
        date_naiss=fake.date_of_birth(),
        ville=fake.city(),
        num_permi=fake.bothify(text='P########'),
        num_cni=fake.bothify(text='CNI#######'),
        telephone=fake.phone_number(),
    )

def create_voiture(utilisateur):
    return Voiture.objects.create(
        utilisateur=utilisateur,
        marque=fake.company(),
        modele=fake.word(),
        annee=fake.year(),
        immatriculation=fake.bothify(text='???-####'),
    )

def create_accident(utilisateur, voiture):
    return Accident.objects.create(
        utilisateur=utilisateur,
        voiture=voiture,
        date=fake.date_time_between(start_date='-1y', end_date='now'),
        description=fake.text(),
        latitude=fake.latitude(),
        longitude=fake.longitude(),
    )

def run():
    for _ in range(10):  # Création de 10 utilisateurs
        utilisateur = create_utilisateur()
        for _ in range(random.randint(1, 3)):  # Chaque utilisateur possède entre 1 et 3 voitures
            voiture = create_voiture(utilisateur)
            for _ in range(random.randint(0, 5)):  # Chaque voiture peut être impliquée dans 0 à 5 accidents
                create_accident(utilisateur, voiture)

if __name__ == '__main__':
    run()
