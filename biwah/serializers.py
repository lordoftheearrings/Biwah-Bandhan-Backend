'''from rest_framework import serializers
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
'''

from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.hashers import make_password
from .models import User, Profile, Kundali
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Hash password if provided
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'phone_number',
            'age',
            'gender',
            'religion',
            'caste',
            'bio',
            'name',
            'profile_image',
            'cover_image',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'profile_image': {'required': False},
            'cover_image': {'required': False},
            'phone_number': {'required': False},
            'age': {'required': False},
            'gender': {'required': False},
            'bio': {'required': False},
            'name': {'required': False},
            'religion': {'required': False},
            'caste': {'required': False},
        }

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
                username = instance.user.username if instance.user.username else "default"

                # Create a file name with the prefix and username
                file_name = f"{prefix}_{username}.{ext}"

                # Save the file to the model field
                image_field = getattr(instance, field_name)
                image_field.save(file_name, image_data)
        except Exception as e:
            raise serializers.ValidationError(f"Error processing image: {str(e)}")

    def create(self, validated_data):
        user = validated_data.pop('user')
        profile = Profile.objects.create(user=user, **validated_data)
        return self._handle_images(profile, validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return self._handle_images(instance, validated_data)

    def _handle_images(self, instance, validated_data):
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

        instance.save()
        return instance

    def validate_phone_number(self, value):
        """
        Validate phone number format (e.g., only numeric characters, correct length).
        """
        if value and not re.match(r'^\d{0,15}$', value):
            raise serializers.ValidationError("Phone number must be numeric and between 10 to 15 digits.")
        return value

class KundaliSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kundali
        fields = [
            'user',
            'birth_year',
            'birth_month',
            'birth_date',
            'birth_hour',
            'birth_minute',
            'birth_second',
            'birth_location',
            'birth_latitude',
            'birth_longitude',
            'kundali_svg',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'birth_year': {'required': False},
            'birth_month': {'required': False},
            'birth_date': {'required': False},
            'birth_hour': {'required': False},
            'birth_minute': {'required': False},
            'birth_second': {'required': False},
            'birth_location': {'required': False},
            'birth_latitude': {'required': False},
            'birth_longitude': {'required': False},
            'kundali_svg': {'required': False},
        }

    def create(self, validated_data):
        user = validated_data.pop('user')
        kundali = Kundali.objects.create(user=user, **validated_data)
        return self._handle_kundali_svg(kundali, validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return self._handle_kundali_svg(instance, validated_data)

    def _handle_kundali_svg(self, instance, validated_data):
        # Handle Kundali SVG if present
        if 'kundali_svg' in validated_data:
            kundali_svg_data = validated_data['kundali_svg']
            if kundali_svg_data:
                instance.kundali_svg = kundali_svg_data

        instance.save()
        return instance

class UserDatabaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    name = serializers.CharField(max_length=50, required=False)
    religion = serializers.CharField(max_length=50, required=False)
    caste = serializers.CharField(max_length=50, required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], required=False)
    bio = serializers.CharField(required=False)
    profile_image = serializers.ImageField(required=False)
    cover_image = serializers.ImageField(required=False)
    birth_year = serializers.IntegerField(required=False)
    birth_month = serializers.IntegerField(required=False)
    birth_date = serializers.IntegerField(required=False)
    birth_hour = serializers.IntegerField(required=False)
    birth_minute = serializers.IntegerField(required=False)
    birth_second = serializers.IntegerField(required=False)
    birth_location = serializers.CharField(max_length=255, required=False)
    birth_latitude = serializers.FloatField(required=False)
    birth_longitude = serializers.FloatField(required=False)
    kundali_svg = serializers.FileField(required=False)

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
        }
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        profile_data = {
            'user': user.id,
            'name': validated_data.pop('name', ''),
            'religion': validated_data.pop('religion', ''),
            'caste': validated_data.pop('caste', ''),
            'phone_number': validated_data.pop('phone_number', ''),
            'age': validated_data.pop('age', None),
            'gender': validated_data.pop('gender', ''),
            'bio': validated_data.pop('bio', ''),
            'profile_image': validated_data.pop('profile_image', None),
            'cover_image': validated_data.pop('cover_image', None),
        }
        profile_serializer = ProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        kundali_data = {
            'user': user.id,
            'birth_year': validated_data.pop('birth_year', None),
            'birth_month': validated_data.pop('birth_month', None),
            'birth_date': validated_data.pop('birth_date', None),
            'birth_hour': validated_data.pop('birth_hour', None),
            'birth_minute': validated_data.pop('birth_minute', None),
            'birth_second': validated_data.pop('birth_second', None),
            'birth_location': validated_data.pop('birth_location', ''),
            'birth_latitude': validated_data.pop('birth_latitude', None),
            'birth_longitude': validated_data.pop('birth_longitude', None),
            'kundali_svg': validated_data.pop('kundali_svg', None),
        }
        kundali_serializer = KundaliSerializer(data=kundali_data)
        kundali_serializer.is_valid(raise_exception=True)
        kundali_serializer.save()

        return {
            'username': user.username,
            'name': profile_data['name'],
            'religion': profile_data['religion'],
            'caste': profile_data['caste'],
            'phone_number': profile_data['phone_number'],
            'age': profile_data['age'],
            'gender': profile_data['gender'],
            'bio': profile_data['bio'],
            'profile_image': profile_data['profile_image'],
            'cover_image': profile_data['cover_image'],
            'birth_year': kundali_data['birth_year'],
            'birth_month': kundali_data['birth_month'],
            'birth_date': kundali_data['birth_date'],
            'birth_hour': kundali_data['birth_hour'],
            'birth_minute': kundali_data['birth_minute'],
            'birth_second': kundali_data['birth_second'],
            'birth_location': kundali_data['birth_location'],
            'birth_latitude': kundali_data['birth_latitude'],
            'birth_longitude': kundali_data['birth_longitude'],
            'kundali_svg': kundali_data['kundali_svg'],
        }

    def update(self, instance, validated_data):
        user_data = {
            'username': validated_data.pop('username', instance.user.username),
            'password': validated_data.pop('password', instance.user.password),
        }
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        profile_data = {
            'user': instance.user.id,
            'name': validated_data.pop('name', instance.profile.name),
            'religion': validated_data.pop('religion', instance.profile.religion),
            'caste': validated_data.pop('caste', instance.profile.caste),
            'phone_number': validated_data.pop('phone_number', instance.profile.phone_number),
            'age': validated_data.pop('age', instance.profile.age),
            'gender': validated_data.pop('gender', instance.profile.gender),
            'bio': validated_data.pop('bio', instance.profile.bio),
            'profile_image': validated_data.pop('profile_image', instance.profile.profile_image),
            'cover_image': validated_data.pop('cover_image', instance.profile.cover_image),
        }
        profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        kundali_data = {
            'user': instance.user.id,
            'birth_year': validated_data.pop('birth_year', instance.kundali.birth_year),
            'birth_month': validated_data.pop('birth_month', instance.kundali.birth_month),
            'birth_date': validated_data.pop('birth_date', instance.kundali.birth_date),
            'birth_hour': validated_data.pop('birth_hour', instance.kundali.birth_hour),
            'birth_minute': validated_data.pop('birth_minute', instance.kundali.birth_minute),
            'birth_second': validated_data.pop('birth_second', instance.kundali.birth_second),
            'birth_location': validated_data.pop('birth_location', instance.kundali.birth_location),
            'birth_latitude': validated_data.pop('birth_latitude', instance.kundali.birth_latitude),
            'birth_longitude': validated_data.pop('birth_longitude', instance.kundali.birth_longitude),
            'kundali_svg': validated_data.pop('kundali_svg', instance.kundali.kundali_svg),
        }
        kundali_serializer = KundaliSerializer(instance.kundali, data=kundali_data, partial=True)
        kundali_serializer.is_valid(raise_exception=True)
        kundali_serializer.save()

        return {
            'username': user_serializer.data['username'],
            'name': profile_serializer.data['name'],
            'religion': profile_serializer.data['religion'],
            'caste': profile_serializer.data['caste'],
            'phone_number': profile_serializer.data['phone_number'],
            'age': profile_serializer.data['age'],
            'gender': profile_serializer.data['gender'],
            'bio': profile_serializer.data['bio'],
            'profile_image': profile_serializer.data['profile_image'],
            'cover_image': profile_serializer.data['cover_image'],
            'birth_year': kundali_serializer.data['birth_year'],
            'birth_month': kundali_serializer.data['birth_month'],
            'birth_date': kundali_serializer.data['birth_date'],
            'birth_hour': kundali_serializer.data['birth_hour'],
            'birth_minute': kundali_serializer.data['birth_minute'],
            'birth_second': kundali_serializer.data['birth_second'],
            'birth_location': kundali_serializer.data['birth_location'],
            'birth_latitude': kundali_serializer.data['birth_latitude'],
            'birth_longitude': kundali_serializer.data['birth_longitude'],
            'kundali_svg': kundali_serializer.data['kundali_svg'],
        }


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
