from rest_framework import serializers
from .models import Utilisateur, Voiture, Accident

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'code_conducteur', 'nom_complet', 'date_naiss', 'ville', 'num_permi', 'num_cni', 'telephone', 'email']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ['id', 'code_conducteur', 'nom_complet', 'date_naiss', 'ville', 'num_permi', 'num_cni', 'telephone', 'email', 'password']

    def create(self, validated_data):
        user = Utilisateur.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            code_conducteur=validated_data['code_conducteur'],
            nom_complet=validated_data['nom_complet'],
            date_naiss=validated_data.get('date_naiss'),
            ville=validated_data.get('ville'),
            num_permi=validated_data.get('num_permi'),
            num_cni=validated_data.get('num_cni'),
            telephone=validated_data.get('telephone')
        )
        return user

class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = ['id', 'utilisateur', 'marque', 'modele', 'annee', 'immatriculation']

class AccidentSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)
    voiture = VoitureSerializer(read_only=True)
    
    class Meta:
        model = Accident
        fields = ['id', 'utilisateur', 'voiture', 'date', 'description', 'latitude', 'longitude']
