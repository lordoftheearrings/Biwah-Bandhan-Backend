from django.db import models

"""
class UserDatabase(models.Model):
    username = models.CharField(max_length=100, unique=True)  # Username must be unique
    password = models.CharField(max_length=100)  # Password is hashed; plaintext should never be stored
    phone_number = models.CharField(max_length=15,null=True, blank=True)  # Optional phone number
    age = models.IntegerField(null=True, blank=True)  # Optional age
    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        blank=True
    )  # Optional gender with predefined choices
    religion = models.CharField(max_length=50, blank=True)  # Optional religion
    caste = models.CharField(max_length=50, blank=True)  # Optional caste
    bio = models.TextField(blank=True)  # Optional bio
    name = models.CharField(max_length=50, blank=True)  # Optional name
    
    # Images are stored in the file system; only paths are stored in the database
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)  

    # Kundali Info          
    birth_year = models.IntegerField(null=True, blank=True)
    birth_month = models.IntegerField(null=True, blank=True)
    birth_date = models.IntegerField(null=True, blank=True)
    birth_hour = models.IntegerField(null=True, blank=True)
    birth_minute = models.IntegerField(null=True, blank=True)
    birth_second = models.IntegerField(null=True, blank=True)
    birth_location = models.CharField(max_length=255, null=True, blank=True)
    birth_latitude = models.FloatField(null=True, blank=True)
    birth_longitude = models.FloatField(null=True, blank=True)
    kundali_svg = models.FileField(max_length=255,upload_to='kundali_svgs/', blank=True, null=True)     

    def __str__(self):
        return self.username
"""
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)  # Username must be unique
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15,null=True, blank=True)  # Optional phone number
    age = models.IntegerField(null=True, blank=True)  # Optional age
    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        blank=True
    )  # Optional gender with predefined choices
    religion = models.CharField(max_length=50, blank=True)  # Optional religion
    caste = models.CharField(max_length=50, blank=True)  # Optional caste
    bio = models.TextField(blank=True)  # Optional bio
    name = models.CharField(max_length=50, blank=True)  # Optional name
    
    # Images are stored in the file system; only paths are stored in the database
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Kundali(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Kundali Info          
    birth_year = models.IntegerField(null=True, blank=True)
    birth_month = models.IntegerField(null=True, blank=True)
    birth_date = models.IntegerField(null=True, blank=True)
    birth_hour = models.IntegerField(null=True, blank=True)
    birth_minute = models.IntegerField(null=True, blank=True)
    birth_second = models.IntegerField(null=True, blank=True)
    birth_location = models.CharField(max_length=255, null=True, blank=True)
    birth_latitude = models.FloatField(null=True, blank=True)
    birth_longitude = models.FloatField(null=True, blank=True)
    kundali_svg = models.FileField(max_length=255,upload_to='kundali_svgs/', blank=True, null=True)

    def __str__(self):
        return self.user.username