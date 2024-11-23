from .models import UserDatabase

def calculate_weighted_score(current_user, potential_match, weights):
    score = 0

    # Age Matching
    if 'age' in weights:
        # Ensure that age is not None, default to 0 if missing
        current_user_age = current_user.age if current_user.age is not None else 0
        potential_match_age = potential_match.age if potential_match.age is not None else 0
        
        # Normalize age difference (assuming max difference is 20 years)
        age_diff = abs(current_user_age - potential_match_age)
        age_score = 1 - (age_diff / 20)  # Normalize between 0 and 1
        score += weights['age'] * max(0, age_score)  # Prevent negative scores

    # Gender Matching (only opposite gender)
    if 'gender' in weights:
        gender_match = 0  # Default no match
        if current_user.gender == 'male' and potential_match.gender == 'female':
            gender_match = 1
        elif current_user.gender == 'female' and potential_match.gender == 'male':
            gender_match = 1
        elif current_user.gender == 'other' and potential_match.gender != 'other':
            gender_match = 1  # If user is 'other', show opposite gender
        
        score += weights['gender'] * gender_match

    return score
