from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from .models import UserDatabase
from .serializers import UserDatabaseSerializer
from .weighted_score import calculate_weighted_score  # Import matchmaking logic
import os

# Helper to construct full image URLs
def build_image_url(image_field):
    if image_field and image_field.name:
        return f"{settings.MEDIA_URL}{image_field.name}"
    return None

# Register View
class UserRegisterView(generics.CreateAPIView):
    queryset = UserDatabase.objects.all()
    serializer_class = UserDatabaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "User registered successfully!",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)

# Login View
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"message": "Username and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDatabase.objects.get(username=username)
            if check_password(password, user.password):
                return Response({
                    "message": "Logged in successfully!",
                    "user": {
                        "username": user.username,
                        "phone_number": user.phone_number,
                        "age": user.age,
                        "gender": user.gender,
                        "religion": user.religion,
                        "caste": user.caste,
                        "bio": user.bio,
                        "profile_image": build_image_url(user.profile_image),
                        "cover_image": build_image_url(user.cover_image),
                        "name": user.name,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid password"},
                                status=status.HTTP_400_BAD_REQUEST)
        except UserDatabase.DoesNotExist:
            return Response({"message": "Invalid username"},
                            status=status.HTTP_400_BAD_REQUEST)

# Profile Update View
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserDatabase.objects.all()
    serializer_class = UserDatabaseSerializer
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        profile_image = request.FILES.get('profile_image', None)
        cover_image = request.FILES.get('cover_image', None)

        # Handle profile image upload
        if profile_image:
            if instance.profile_image:
                try:
                    os.remove(instance.profile_image.path)
                except FileNotFoundError:
                    pass
            instance.profile_image = profile_image

        # Handle cover image upload
        if cover_image:
            if instance.cover_image:
                try:
                    os.remove(instance.cover_image.path)
                except FileNotFoundError:
                    pass
            instance.cover_image = cover_image

        # Update other fields
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({"message": "Validation failed", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)

        return Response({
            "message": "Profile updated successfully!",
            "user": {
                "username": instance.username,
                "phone_number": instance.phone_number,
                "age": instance.age,
                "gender": instance.gender,
                "religion": instance.religion,
                "caste": instance.caste,
                "bio": instance.bio,
                "profile_image": build_image_url(instance.profile_image),
                "cover_image": build_image_url(instance.cover_image),
                "name": instance.name,
            }
        }, status=status.HTTP_200_OK)

# Matchmaking View
class MatchmakingView(APIView):
    def get(self, request, username):
        try:
            current_user = UserDatabase.objects.get(username=username)
        except UserDatabase.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Exclude current user from potential matches
        potential_matches = UserDatabase.objects.exclude(username=username)
        
        # Define example weights (customize based on your app logic)
        weights = {
            'age': 0.4,
            'religion': 0.3,
            'caste': 0.2,
            # Add more criteria as needed
        }

        matches = []
        for user in potential_matches:
            compatibility_score = calculate_weighted_score(current_user, user, weights)
            matches.append({
                'username': user.username,
                'name': user.name,
                'score': compatibility_score,
                'profile_image': build_image_url(user.profile_image),
                'bio': user.bio
            })

        # Sort matches by score in descending order
        sorted_matches = sorted(matches, key=lambda x: x['score'], reverse=True)

        return Response({"matches": sorted_matches}, status=status.HTTP_200_OK)
