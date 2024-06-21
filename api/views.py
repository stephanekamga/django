from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Utilisateur, Accident
from .serializers import UtilisateurSerializer, RegistrationSerializer, AccidentSerializer

user = get_user_model()

class RegistrationView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UtilisateurViewSet(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response(status=400)
        
class AccidentCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Assume that the request contains all the necessary data to create an Accident entry
        data = request.data
        utilisateur_id = data.get('utilisateur_id')
        voiture_id = data.get('voiture_id')

        try:
            utilisateur = Utilisateur.objects.get(id=utilisateur_id)
            voiture = Voiture.objects.get(id=voiture_id)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur not found"}, status=status.HTTP_404_NOT_FOUND)
        except Voiture.DoesNotExist:
            return Response({"error": "Voiture not found"}, status=status.HTTP_404_NOT_FOUND)

        accident_data = {
            'utilisateur': utilisateur.id,
            'voiture': voiture.id,
            'date': data.get('date'),
            'description': data.get('description'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
        }
        
        serializer = AccidentSerializer(data=accident_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccidentListView(generics.ListCreateAPIView):
    queryset = Accident.objects.all()
    serializer_class = AccidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    def get_queryset(self):
        return Accident.objects.all() # No filter on utilisateur, return all accidents

# class AccidentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Accident.objects.all()
#     serializer_class = AccidentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(utilisateur=self.request.user)
