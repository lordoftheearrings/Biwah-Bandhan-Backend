from faker import Faker
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserDatabase  
import random

fake = Faker()

# Function to simulate data
def generate_fake_user_data(num_users):
    for _ in range(num_users):
        # Generating random user data
        username = fake.user_name()
        name = fake.name()
        bio = fake.text(max_nb_chars=50)
        age = random.randint(18, 55)  
        gender = random.choice([ 'Other'])
        caste = random.choice(['Newar', 'Brahmin', 'Chhetri'])  # Update with actual options
        religion = random.choice(['Hindu', 'Muslim', 'Christian','Buddhism','Jewish'])  # Update with actual options
        phone_number = random.randint(1000000000, 9999999999)
        password='samplepw'
        # Generate a hashed password for the user
        hashed_password = make_password(password)  # You can change the password as needed
        
        # Create or update the user in the database
        user = UserDatabase.objects.create(
            username=username,
            name=name,
            bio=bio,
            age=age,
            gender=gender,
            caste=caste,
            religion=religion,
            phone_number=phone_number,
            password=hashed_password,  # Already hashed
            # Add other fields if needed
        )
        user.save()
        print(f"User {username} created.")

generate_fake_user_data(40)
