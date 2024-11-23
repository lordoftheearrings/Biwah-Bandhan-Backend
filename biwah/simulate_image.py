import random
import os
from biwah.models import UserDatabase  # Adjust this based on your actual model

# List of profile images for male, female, and other genders (stored in the 'media/profiles/' folder)
male_images = ['hitler.jpg', 'male2.jpg', 'mao.jpg', 'modi.jpg', 'oli.jpg', 'putin.jpg', 'stalin.jpg', 'Screenshot (83).png']
female_images = ['f1.jpg', 'f2.jpg', 'f3.jpg', 'f4.jpg', 'f5.jpg', 'f6.jpg', 'syd.jpg', 'ana.jpg']

# Define the base directory for profile images and cover images
PROFILE_IMAGE_DIR = 'C:/Users/Hp/Documents/Biwah Bandhan Backend/biwah_bandhan/media/profile_images/'
COVER_IMAGE_DIR = 'C:/Users/Hp/Documents/Biwah Bandhan Backend/biwah_bandhan/media/cover_images/'

# Function to construct the full local file path
def build_full_path(image_name, image_type):
    if image_type == "profile":
        return os.path.join(PROFILE_IMAGE_DIR, image_name)
    elif image_type == "cover":
        return os.path.join(COVER_IMAGE_DIR, image_name)
    return None

# Function to update the profile image URL randomly based on gender
def update_profile_images():
    users = UserDatabase.objects.all()  # Get all users from the database
    
    for user in users:
        # Check the user's gender and assign a random profile image
        if user.gender == 'Male':
            user.profile_image = build_full_path('profile_shrijal.jpg', "profile")  # Full local path for profile image
        elif user.gender == 'Female':
            user.profile_image = build_full_path('gal.jpg', "profile")  # Full local path for profile image
        elif user.gender == 'Other':
            user.profile_image = build_full_path('1000377902.jpg', "profile")  # Default image for Other gender
        
        # Save the updated profile image back to the database
        user.save()  
        print(f"Updated {user.username}'s profile image to {user.profile_image}")

# Function to update the cover image URL randomly based on gender
def update_cover_image():
    users = UserDatabase.objects.all()  # Get all users from the database
    for user in users:
        # Check the user's gender and assign a random cover image
        if user.gender == 'Male':
            random_image = random.choice(male_images)
            user.cover_image = build_full_path(random_image, "cover")  # Full local path for cover image
        elif user.gender == 'Female':
            random_image = random.choice(female_images)
            user.cover_image = build_full_path(random_image, "cover")  # Full local path for cover image
        elif user.gender == 'Other':
            user.cover_image = build_full_path('geh.jpg', "cover")  # Default cover image for Other gender
        
        # Save the updated cover image back to the database
        user.save()  
        print(f"Updated {user.username}'s cover image to {user.cover_image}")

# Run the functions to update profile and cover images
update_profile_images()
update_cover_image()
