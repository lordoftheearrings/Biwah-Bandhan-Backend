from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.hashers import make_password
from biwah.models import UserDatabase
import random

class Command(BaseCommand):
    help = 'Simulate data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_users = 1000  # Number of users to simulate

        def generate_fake_user_data(num_users):
            for _ in range(num_users):
                # Generating random user data
                username = fake.user_name()
                name = fake.name()
                bio = fake.text(max_nb_chars=100)
                age = random.randint(18, 55)
                gender = random.choice(['Male', 'Female', 'Other'])
                caste = random.choice([
                    'Bahun', 'Chhetri', 'Thakuri', 'Magar', 'Tharu', 'Tamang', 
                    'Newar', 'Rai', 'Gurung', 'Limbu', 'Sherpa', 'Yadav', 'Kami', 
                    'Damai', 'Sarki'
                ])
                religion = random.choice([
                    'Hindu', 'Buddhist', 'Islam', 'Christian', 'Jain', 'Kiranti'
                ])
                phone_number = random.randint(000000,99999)  # Random phone number
                password = 'samplepw'
                hashed_password = make_password(password)  # Password should be hashed

                # Gotra choice
                gotra = random.choice([
                    'Bharadwaj', 'Kashyap', 'Vashishtha', 'Vishwamitra', 'Gautam', 
                    'Jamadagni', 'Atri', 'Agastya', 'Bhrigu', 'Angirasa', 'Parashar', 'Mudgala'
                ])

                # Height and weight
                height = random.randint(150, 180)  # Random height between 150cm and 180cm
                weight = random.randint(45, 100)  # Random weight between 45kg and 100kg

                # Zodiac sign
                zodiac = random.choice([
                    'Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya', 
                    'Tula', 'Vrischika', 'Dhanu', 'Makara', 'Kumbha', 'Meena'
                ])

                # Education and profession
                education = random.choice([
                    'SEE', 'High School or +2', 'Diploma', 'Bachelors', 'Masters', 'PhD'
                ])
                profession = fake.job()

                # Family type and address
                family_type = random.choice(['Nuclear', 'Joint'])
                address = fake.address()

                # Complexion, marital status, habits
                complexion = random.choice(['Fair', 'Medium', 'Dark'])
                marital_status = random.choice(['Single', 'Divorce', 'Married'])
                habits_drinking = random.choice(['Alcoholic', 'Non-Alcoholic'])
                habits_eating = random.choice(['Veg', 'Non-Veg'])
                habits_smoking = random.choice(['Smoker', 'Non-Smoker'])

                # Kundali info (date and time details)
                birth_year = random.randint(1950, 2020)
                birth_month = random.randint(1, 12)
                birth_date = random.randint(1, 28)  # Avoid issues with different month lengths
                birth_hour = random.randint(0, 23)
                birth_minute = random.randint(0, 59)
                birth_second = random.randint(0, 59)
                birth_location = fake.city()
                birth_latitude = fake.latitude()
                birth_longitude = fake.longitude()

                # Create the user and save to database
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
                    gotra=gotra,
                    height=height,
                    weight=weight,
                    zodiac=zodiac,
                    education=education,
                    profession=profession,
                    family_type=family_type,
                    address=address,
                    complexion=complexion,
                    marital_status=marital_status,
                    habits_drinking=habits_drinking,
                    habits_eating=habits_eating,
                    habits_smoking=habits_smoking,
                    birth_year=birth_year,
                    birth_month=birth_month,
                    birth_date=birth_date,
                    birth_hour=birth_hour,
                    birth_minute=birth_minute,
                    birth_second=birth_second,
                    birth_location=birth_location,
                    birth_latitude=birth_latitude,
                    birth_longitude=birth_longitude
                )
                user.save()
                print(f"User {username} created with all fields.")

        generate_fake_user_data(num_users)
