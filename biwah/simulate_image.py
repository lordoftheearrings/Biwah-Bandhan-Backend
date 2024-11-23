# Import necessary modules

import random

# Setup Django environment if running outside of Django shell


from biwah.models import UserDatabase  # Adjust this based on your actual model

# List of profile images for male, female, and other genders (stored in the 'media/profiles/' folder)
male_images = ['hitler.jpg','male2.jpg','mao.jpg','modi.jpg','oli.jpg','putin.jpg','stalin.jpg','Screenshot (83).png']
female_images = ['f1.jpg','f2.jpg','f3.jpg','f4.jpg','f5.jpg','f6.jpg','syd.jpg','ana.jpg']


# Function to update the profile image URL randomly based on gender
def update_profile_images():
    users = UserDatabase.objects.all()  # Get all users from the database
    
    for user in users:
        # Check the user's gender and assign a random profile image
        if user.gender == 'Male':
            user.profile_image = f'/media/profile_images/profile_shrijal.jpg'
        elif user.gender == 'Female':
            user.profile_image = f'/media/profile_images/gal.jpg'
        elif user.gender == 'Other':
            user.profile_image = f'/media/profile_images/1000377902.jpg'
        
        
        # Save the updated profile_image back to the database
        user.save()  
        print(f"Updated {user.username}'s profile image to {user.profile_image}")

# Run the function to update profile images
update_profile_images()

def update_cover_image():
    users=UserDatabase.objects.all()
    for user in users:
        # Check the user's gender and assign a random profile image
        if user.gender == 'Male':
            user.cover_image = f'/media/cover_images/{random.choice(male_images)}'
        elif user.gender == 'Female':
            user.cover_image = f'/media/cover_images/{random.choice(female_images)}'
        elif user.gender == 'Other':
            user.cover_image = f'/media/cover_images/geh.jpg'
        
        
        # Save the updated profile_image back to the database
        user.save()  
        print(f"Updated {user.username}'s cover image to {user.cover_image}")

# Run the function to update profile images
update_cover_image()
