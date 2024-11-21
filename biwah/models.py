from django.db import models

class UserDatabase(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.IntegerField( null=True,blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True
    )
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    name = models.CharField(max_length=50, blank=True)
    
    # Store profile image and cover image as BinaryFields (bytea)
    profile_image = models.ImageField(upload_to='profile_images/',blank=True, null=True)  # Image stored in bytea format
    cover_image = models.ImageField(upload_to='cover_images/',blank=True, null=True)  # Image stored in bytea format

    def __str__(self):
        return self.username
