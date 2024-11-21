from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.base import ContentFile
from django.conf import settings
from .models import UserDatabase
from .serializers import UserDatabaseSerializer
import base64
import os

# Helper to construct image URLs
def build_image_url(image_field):
    if image_field and image_field.name:
        return f"{settings.MEDIA_URL}{image_field.name}"
    return None

# Register View
class UserRegisterView(generics.CreateAPIView):
    queryset = UserDatabase.objects.all()
    serializer_class = UserDatabaseSerializer

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)  # Debugging incoming data

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
            return Response({
                "message": "Username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({
                    "message": "Invalid password"
                }, status=status.HTTP_400_BAD_REQUEST)

        except UserDatabase.DoesNotExist:
            return Response({
                "message": "Invalid username"
            }, status=status.HTTP_400_BAD_REQUEST)

# Profile Update View
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserDatabase.objects.all()
    serializer_class = UserDatabaseSerializer
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        # Handle image fields (decode base64 if provided)
        profile_image = request.data.get('profile_image', None)
        cover_image = request.data.get('cover_image', None)

        if profile_image:
            image_data = base64.b64decode(profile_image)
            file_name = f"profile_{instance.username}.jpg"
            instance.profile_image.save(file_name, ContentFile(image_data), save=False)

        if cover_image:
            image_data = base64.b64decode(cover_image)
            file_name = f"cover_{instance.username}.jpg"
            instance.cover_image.save(file_name, ContentFile(image_data), save=False)

        # Update other fields
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
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
