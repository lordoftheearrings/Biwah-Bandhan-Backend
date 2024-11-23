from .models import UserDatabase

def calculate_weighted_score(user, profile, weights):
    score = 0

    # Age difference condition
    age_difference = abs(user.age - profile.age)  # Calculate absolute age difference
    if age_difference <= 3:
        score += weights['age'] * 3  # If age difference is 2 or less, give a high score
    elif age_difference <= 6:
        score += weights['age']  # If age difference is 3-5, give a medium score
    else:
        score += weights['age'] * 0.2  # If age difference is greater than 5, give a lower score

    # Religion condition
    if profile.religion == user.religion:
        score += weights['religion']  # Match on religion

    # Caste condition
    if profile.caste == user.caste:
        score += weights['caste']  # Match on caste

    # You can add more conditions here, for example:
    # - Education level
    # - Interests or hobbies
    # - Location proximity (if you want to use geo-location)

    return score
