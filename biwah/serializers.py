from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from .models import UserDatabase
import os
import re

class UserDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDatabase
        fields = [
            'username', 
            'password', 
            'name',
            'religion',
            'caste',
            'phone_number', 
            'age', 
            'gender', 
            'bio', 
            'profile_image', 
            'cover_image', 
            'birth_year',
            'birth_month',
            'birth_date',
            'birth_hour',
            'birth_minute',
            'birth_second',
            'birth_location',
            'birth_latitude',
            'birth_longitude',
            'kundali_svg',  # Field for storing the Kundali SVG data
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
            'religion': {'required': False},
            'caste': {'required': False},
            'birth_year': {'required': False},
            'birth_month': {'required': False},
            'birth_date': {'required': False},
            'birth_hour': {'required': False},
            'birth_minute': {'required': False},
            'birth_second': {'required': False},
            'birth_location': {'required': False},
            'birth_latitude': {'required': False},
            'birth_longitude': {'required': False},
            'kundali_svg': {'required': False},  # New field for storing SVG
        }

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        # Create user instance and handle images and kundali data
        return self._handle_images_and_kundali(UserDatabase.objects.create(**validated_data), validated_data)

    def update(self, instance, validated_data):
        # Hash password if provided
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)

        # Update the instance with provided data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle images and kundali data
        return self._handle_images_and_kundali(instance, validated_data)

    def _handle_images_and_kundali(self, instance, validated_data):
        """
        Handle image file uploads and saving of Kundali SVG data.
        """
        # Handle profile image
        if 'profile_image' in validated_data:
            profile_image_data = validated_data['profile_image']
            if profile_image_data:
                self._save_image(instance, 'profile_image', profile_image_data, 'profile')

        # Handle cover image
        if 'cover_image' in validated_data:
            cover_image_data = validated_data['cover_image']
            if cover_image_data:
                self._save_image(instance, 'cover_image', cover_image_data, 'cover')

        # Handle Kundali SVG if present
        if 'kundali_svg' in validated_data:
            kundali_svg_data = validated_data['kundali_svg']
            if kundali_svg_data:
                instance.kundali_svg = kundali_svg_data

        instance.save()
        return instance

    def _save_image(self, instance, field_name, image_data, prefix):
        """
        Save uploaded image to the corresponding field in the model.
        """
        try:
            if isinstance(image_data, InMemoryUploadedFile):  # Ensure it's an uploaded file
                ext = image_data.name.split('.')[-1]  # Get file extension (e.g., jpg, png)
                
                # Validate image type
                allowed_formats = ['jpeg', 'png', 'jpg']
                if ext.lower() not in allowed_formats:
                    raise serializers.ValidationError("Unsupported image format. Only JPEG, PNG, and JPG are allowed.")

                # Check image size (e.g., limit to 10 MB)
                if image_data.size > 10 * 1024 * 1024:  # 10 MB limit
                    raise serializers.ValidationError("Image file is too large. Maximum size is 10 MB.")

                # Ensure username is available
                username = instance.username if instance.username else "default"

                # Create a file name with the prefix and username
                file_name = f"{prefix}_{username}.{ext}"

                # Save the file to the model field
                image_field = getattr(instance, field_name)
                image_field.save(file_name, image_data)
        except Exception as e:
            raise serializers.ValidationError(f"Error processing image: {str(e)}")

    def validate_phone_number(self, value):
        """
        Validate phone number format (e.g., only numeric characters, correct length).
        """
        if value and not re.match(r'^\d{0,15}$', value):
            raise serializers.ValidationError("Phone number must be numeric and between 10 to 15 digits.")
        return value

    def validate_profile_image(self, value):
        return value

    def validate_cover_image(self, value):
        return value


class GunaMilanSerializer(serializers.Serializer):
    year_boy = serializers.IntegerField()
    month_boy = serializers.IntegerField()
    day_boy = serializers.IntegerField()
    hour_boy = serializers.IntegerField()
    minute_boy = serializers.IntegerField()
    second_boy = serializers.IntegerField()
    latitude_boy = serializers.FloatField()
    longitude_boy = serializers.FloatField()

    year_girl = serializers.IntegerField()
    month_girl = serializers.IntegerField()
    day_girl = serializers.IntegerField()
    hour_girl = serializers.IntegerField()
    minute_girl = serializers.IntegerField()
    second_girl = serializers.IntegerField()
    latitude_girl = serializers.FloatField()
    longitude_girl = serializers.FloatField()