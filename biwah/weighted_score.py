
def calculate_weighted_score(user, profile, weights, preferences):
    score = 0

    # Age difference condition
    age_difference = abs(user.age - profile.age)  # Calculate absolute age difference
    if preferences['age_min'] and preferences['age_max']:
        if preferences['age_min'] <= profile.age <= preferences['age_max']:
            score += weights['age']  # Apply weight if the age falls within preferred range
        elif age_difference <= 3:
            score += weights['age'] * 3  # If age difference is 2 or less, give a high score
        elif age_difference <= 6:
            score += weights['age']  # If age difference is 3-5, give a medium score
        else:
            score += weights['age'] * 0.1  # If age difference is greater than 5, give a lower score

    # Religion condition
    if preferences['religion'] and profile.religion == preferences['religion']:
        score += weights['religion']  # Match on religion

    # Caste condition
    if preferences['caste'] and profile.caste == preferences['caste']:
        score += weights['caste']  # Match on caste

    # Gotra condition
    if preferences['gotra']:
        if profile.gotra == preferences['gotra']:
            score += weights['gotra']  # Match on gotra
        else:
            score -= weights['gotra']   # Match on gotra

    # Height condition
    
    if preferences['height_min'] is not None and preferences['height_max'] is not None:
        if preferences['height_min'] <= profile.height <= preferences['height_max']:
            score += weights['height']  # Match on height

    # Weight condition
    if preferences['weight_min'] is not None and preferences['weight_max'] is not None:
        if preferences['weight_min'] <= profile.weight <= preferences['weight_max']:
            score += weights['weight']  # Match on weight

    # Drinking habits condition
    if preferences['drinking'] and profile.habits_drinking == preferences['drinking']:
        score += weights['habits']  # Match on drinking habits

    # Eating habits condition
    if preferences['eating'] and profile.habits_eating == preferences['eating']:
        score += weights['habits']  # Match on eating habits

    # Smoking habits condition
    if preferences['smoking'] and profile.habits_smoking == preferences['smoking']:
        score += weights['habits']  # Match on smoking habits

    # Return the total score
    return score
