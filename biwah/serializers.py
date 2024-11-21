from rest_framework import serializers
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from .models import UserDatabase
import base64
import os

class UserDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDatabase
        fields = [
            'username', 
            'password', 
            'phone_number', 
            'age', 
            'gender', 
            'bio', 
            'profile_image', 
            'cover_image', 
            'name'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_image': {'required': False},
            'cover_image': {'required': False},
            'phone_number': {'required': False},
            'age': {'required': False},
            'gender': {'required': False},
            'bio': {'required': False},
            'name': {'required': False},
        }

    def create(self, validated_data):
        # Extract and hash password
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        # Save the user and handle images
        return self._handle_images(UserDatabase.objects.create(**validated_data), validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            validated_data['password'] = make_password(password)

        # Update user instance with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return self._handle_images(instance, validated_data)

    def _handle_images(self, instance, validated_data):
        """
        Handle image uploads (base64 to file conversion).
        """
        if 'profile_image' in validated_data:
            profile_image = validated_data['profile_image']
            if profile_image:
                instance.profile_image.save(
                    self._get_image_name('profile', instance.username),
                    ContentFile(base64.b64decode(profile_image))
                )

        if 'cover_image' in validated_data:
            cover_image = validated_data['cover_image']
            if cover_image:
                instance.cover_image.save(
                    self._get_image_name('cover', instance.username),
                    ContentFile(base64.b64decode(cover_image))
                )

        instance.save()
        return instance

    def _get_image_name(self, prefix, username):
        """
        Generate a unique image name based on prefix and username.
        """
        return f"{prefix}_{username}.jpg"
