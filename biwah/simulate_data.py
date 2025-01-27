import os
import django
import random
from faker import Faker
from django.contrib.auth.hashers import make_password
from .models import User, Profile  # Adjust to your app's name

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biwah_bandhan.settings')  # Update with your project name
django.setup()

fake = Faker()

# Function to simulate data
def generate_fake_user_data(num_users):
    for _ in range(num_users):
        username = fake.unique.user_name()
        password = make_password("samplepw")  # Hashed password
        user = User.objects.create(username=username, password=password)

        name = fake.name()
        bio = fake.text(max_nb_chars=50)
        age = random.randint(18, 55)
        gender = random.choice(['Male', 'Female', 'Other'])
        caste = random.choice(['Newar', 'Brahmin', 'Chhetri'])
        religion = random.choice(['Hindu', 'Muslim', 'Christian', 'Buddhism', 'Jewish'])
        phone_number = fake.phone_number()

        profile = Profile.objects.create(
            user=user,
            name=name,
            bio=bio,
            age=age,
            gender=gender,
            caste=caste,
            religion=religion,
            phone_number=phone_number
        )
        profile.save()
        print(f"User {username} with profile created.")

# Generate 40 fake users
if __name__ == "__main__":
    generate_fake_user_data(40)
