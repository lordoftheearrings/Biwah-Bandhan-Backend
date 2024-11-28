from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from .models import UserDatabase
from .serializers import UserDatabaseSerializer
from .weighted_score import calculate_weighted_score  
import os
from kundali.Kundali import generate_kundali_svg

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
                "name": instance.name,
                "phone_number": instance.phone_number,
                "age": instance.age,
                "gender": instance.gender,
                "religion": instance.religion,
                "caste": instance.caste,
                "bio": instance.bio,
                "profile_image": build_image_url(instance.profile_image),
                "cover_image": build_image_url(instance.cover_image),
                
            }
        }, status=status.HTTP_200_OK)

# Matchmaking View

class MatchmakingView(APIView):

    def get(self, request, username):
        # Extract offset and limit for pagination (default to 0 and 10)
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 15))

        try:
            # Get the current user
            current_user = UserDatabase.objects.get(username=username)
        except UserDatabase.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Determine the opposite gender
        # Determine the opposite gender
        if current_user.gender == 'Male':
            opposite_gender = 'Female'
        elif current_user.gender == 'Female':
            opposite_gender = 'Male'
        else:  # For 'Other'
            opposite_gender = 'Other'

# Exclude the current user and filter by opposite gender
        potential_matches = UserDatabase.objects.exclude(username=username).filter(gender=opposite_gender).order_by('?')[offset:offset + limit]

        

        

        # Calculate scores for potential matches
        weights = {
            'age': 10,
            'religion': 10,
            'caste': 5,
        }

        matches = []
        for user in potential_matches:
            score = calculate_weighted_score(current_user, user, weights)
            matches.append({'username': user.username, 'score': score})

        # Sort matches by compatibility score (ascending order for best matches)
        sorted_matches = sorted(matches, key=lambda x: x['score'])

        # Return only the usernames
        return Response({"matches": [match['username'] for match in sorted_matches]}, status=status.HTTP_200_OK)
    



