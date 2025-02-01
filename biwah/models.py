from django.db import models


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

    # Gotra options
    gotra = models.CharField(
        max_length=50, 
        choices=[
            ('Bharadwaj', 'Bharadwaj'), 
            ('Kashyap', 'Kashyap'), 
            ('Vashishtha', 'Vashishtha'), 
            ('Vishwamitra', 'Vishwamitra'), 
            ('Gautam', 'Gautam'), 
            ('Jamadagni', 'Jamadagni'), 
            ('Atri', 'Atri'), 
            ('Agastya', 'Agastya'), 
            ('Bhrigu', 'Bhrigu'), 
            ('Angirasa', 'Angirasa'), 
            ('Parashar', 'Parashar'), 
            ('Mudgala', 'Mudgala')
        ],
        blank=True
    )
    
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Height in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Weight in kg

    zodiac = models.CharField(
        max_length=20, 
        choices=[
            ('Mesha', 'Mesha (Aries)'), 
            ('Vrishabha', 'Vrishabha (Taurus)'), 
            ('Mithuna', 'Mithuna (Gemini)'), 
            ('Karka', 'Karka (Cancer)'), 
            ('Simha', 'Simha (Leo)'), 
            ('Kanya', 'Kanya (Virgo)'), 
            ('Tula', 'Tula (Libra)'), 
            ('Vrischika', 'Vrischika (Scorpio)'), 
            ('Dhanu', 'Dhanu (Sagittarius)'), 
            ('Makara', 'Makara (Capricorn)'), 
            ('Kumbha', 'Kumbha (Aquarius)'), 
            ('Meena', 'Meena (Pisces)')
        ],
        blank=True
    )

    education = models.TextField(blank=True)  # Education details (you can expand this if needed)
    profession = models.CharField(max_length=100, blank=True)  # Profession
    family_type = models.CharField(
        max_length=10, 
        choices=[('Nuclear', 'Nuclear'), ('Joint', 'Joint')], 
        blank=True
    )   
    address = models.TextField(blank=True)  # Address
    complexion = models.CharField(max_length=50, blank=True)  # Complexion
    marital_status = models.CharField(
        max_length=20, 
        choices=[('Single', 'Single'), ('Divorce', 'Divorce'), ('Married', 'Married')], 
        blank=True
    )
    habits_drinking = models.CharField(
        max_length=20, 
        choices=[('Alcoholic', 'Alcoholic'), ('Non-Alcoholic', 'Non-Alcoholic')], 
        blank=True
    )
    habits_eating = models.CharField(
        max_length=20, 
        choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg')], 
        blank=True
    )
    habits_smoking = models.CharField(
        max_length=20, 
        choices=[('Smoker', 'Smoker'), ('Non-Smoker', 'Non-Smoker')], 
        blank=True
    )


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



class UserPreferences(models.Model):
    user = models.OneToOneField(UserDatabase, on_delete=models.CASCADE, related_name='preferences')

    p_age_min = models.IntegerField(null=True, blank=True)  # Minimum age preference
    p_age_max = models.IntegerField(null=True, blank=True)  # Maximum age preference

    p_religion = models.CharField(max_length=50, blank=True)  # Preferred religion
    p_caste = models.CharField(max_length=50, blank=True)  # Preferred caste

    p_gotra = models.CharField(
        max_length=50,
        choices=[
            ('Bharadwaj', 'Bharadwaj'),
            ('Kashyap', 'Kashyap'),
            ('Vashishtha', 'Vashishtha'),
            ('Vishwamitra', 'Vishwamitra'),
            ('Gautam', 'Gautam'),
            ('Jamadagni', 'Jamadagni'),
            ('Atri', 'Atri'),
            ('Agastya', 'Agastya'),
            ('Bhrigu', 'Bhrigu'),
            ('Angirasa', 'Angirasa'),
            ('Parashar', 'Parashar'),
            ('Mudgala', 'Mudgala')
        ],
        blank=True
    )  # Preferred gotra

    p_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Preferred height in cm
    p_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Preferred weight in kg


    p_habits_drinking = models.CharField(
        max_length=20,
        choices=[('Alcoholic', 'Alcoholic'), ('Non-Alcoholic', 'Non-Alcoholic')],
        blank=True
    )  # Preferred drinking habits

    p_habits_eating = models.CharField(
        max_length=20,
        choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg')],
        blank=True
    )  # Preferred eating habits

    p_habits_smoking = models.CharField(
        max_length=20,
        choices=[('Smoker', 'Smoker'), ('Non-Smoker', 'Non-Smoker')],
        blank=True
    )  # Preferred smoking habits

    def __str__(self):
        return f"Preferences for {self.user.username}"
    
class WeightedScore (models.Model):


    def __str__(self):
        return f""