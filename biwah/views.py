from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from .models import UserDatabase
from chat.models import MatchRequest
from .serializers import UserDatabaseSerializer
from .weighted_score import calculate_weighted_score  
import os
from django.db.models import Q
from kundali.Kundali import generate_kundali_svg
from django.core.paginator import Paginator, EmptyPage

# Helper to construct full image URLs
def build_image_url(image_field):
    if image_field and image_field.name:
        return f"{settings.MEDIA_URL}{image_field.name}"
    return None

# Register View
class UserRegisterView(generics.CreateAPIView):
    queryset = UserDatabase.objects.all()
    serializer_class = UserDatabaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "User registered successfully!",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)

# Login View
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"message": "Username and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDatabase.objects.get(username=username)
            if check_password(password, user.password):
                return Response({
                    "message": "Logged in successfully!",
                    "user": {
                        "username": user.username,
                        "phone_number": user.phone_number,
                        "age": user.age,
                        "gender": user.gender,
                        "religion": user.religion,
                        "caste": user.caste,
                        "bio": user.bio,
                        "profile_image": build_image_url(user.profile_image),
                        "cover_image": build_image_url(user.cover_image),
                        "name": user.name,
                        "gotra": user.gotra,
                        "height": user.height,
                        "weight": user.weight,
                        "zodiac": user.zodiac,
                        "education": user.education,
                        "profession": user.profession,
                        "family_type": user.family_type,
                        "address": user.address,
                        "complexion": user.complexion,
                        "marital_status": user.marital_status,
                        "habits_drinking": user.habits_drinking,
                        "habits_eating": user.habits_eating,
                        "habits_smoking": user.habits_smoking,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid password"},
                                status=status.HTTP_400_BAD_REQUEST)
        except UserDatabase.DoesNotExist:
            return Response({"message": "Invalid username"},
                            status=status.HTTP_400_BAD_REQUEST)

# Profile Update View
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserDatabase.objects.all()
    serializer_class = UserDatabaseSerializer
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        profile_image = request.FILES.get('profile_image', None)
        cover_image = request.FILES.get('cover_image', None)

        # Handle profile image upload
        if profile_image:
            if instance.profile_image:
                try:
                    os.remove(instance.profile_image.path)
                except FileNotFoundError:
                    pass
            instance.profile_image = profile_image

        # Handle cover image upload
        if cover_image:
            if instance.cover_image:
                try:
                    os.remove(instance.cover_image.path)
                except FileNotFoundError:
                    pass
            instance.cover_image = cover_image

        # Update other fields
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({"message": "Validation failed", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)

        return Response({
            "message": "Profile updated successfully!",
            "user": {
                "username": instance.username,
                "name": instance.name,
                "phone_number": instance.phone_number,
                "age": instance.age,
                "gender": instance.gender,
                "religion": instance.religion,
                "caste": instance.caste,
                "bio": instance.bio,
                "profile_image": build_image_url(instance.profile_image),
                "cover_image": build_image_url(instance.cover_image),
                "kundali_svg":instance.kundali_svg,
                "gotra": instance.gotra,
                "height": instance.height,
                "weight": instance.weight,
                "zodiac": instance.zodiac,
                "education": instance.education,
                "profession": instance.profession,
                "family_type": instance.family_type,
                "address": instance.address,
                "complexion": instance.complexion,
                "marital_status": instance.marital_status,
                "habits_drinking": instance.habits_drinking,
                "habits_eating": instance.habits_eating,
                "habits_smoking": instance.habits_smoking,
                
            }
        }, status=status.HTTP_200_OK)
    
class UserProfileUpdateView2(generics.RetrieveUpdateAPIView):
    queryset = UserDatabase.objects.all()
    serializer_class = UserDatabaseSerializer
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        profile_image = request.FILES.get('profile_image', None)
        cover_image = request.FILES.get('cover_image', None)

        # Handle profile image upload
        if profile_image:
            if instance.profile_image:
                try:
                    os.remove(instance.profile_image.path)
                except FileNotFoundError:
                    pass
            instance.profile_image = profile_image

        # Handle cover image upload
        if cover_image:
            if instance.cover_image:
                try:
                    os.remove(instance.cover_image.path)
                except FileNotFoundError:
                    pass
            instance.cover_image = cover_image

        # Update other fields
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({"message": "Validation failed", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)

        return Response({
            "message": "Profile updated successfully!",
            "user": {
                "username": instance.username,
                "name": instance.name,
                "phone_number": instance.phone_number,
                "age": instance.age,
                "gender": instance.gender,
                "religion": instance.religion,
                "caste": instance.caste,
                "bio": instance.bio,
                "profile_image": build_image_url(instance.profile_image),
                "cover_image": build_image_url(instance.cover_image),
                "gotra": instance.gotra,
                "height": instance.height,
                "weight": instance.weight,
                "zodiac": instance.zodiac,
                "education": instance.education,
                "profession": instance.profession,
                "family_type": instance.family_type,
                "address": instance.address,
                "complexion": instance.complexion,
                "marital_status": instance.marital_status,
                "habits_drinking": instance.habits_drinking,
                "habits_eating": instance.habits_eating,
                "habits_smoking": instance.habits_smoking,
                
                
            }
        }, status=status.HTTP_200_OK)
        

# Matchmaking View

class MatchmakingView(APIView):

    def get(self, request, username):
        # Extract offset and limit for pagination (default to 0 and 10)
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 13))

        try:
            # Get the current user
            current_user = UserDatabase.objects.get(username=username)
        except UserDatabase.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user_preferences = UserPreferences.objects.get(user=current_user)
         # Fetch user preferences from the database
        # try:
        #     user_preferences = UserPreferences.objects.get(user=current_user)
        # except UserPreferences.DoesNotExist:
        #     return Response({"message": "User preferences not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Determine the opposite gender
        # Determine the opposite gender
        if current_user.gender == 'Male':
            opposite_gender = 'Female'
        elif current_user.gender == 'Female':
            opposite_gender = 'Male'
        else:  
            opposite_gender = 'Other'

# Exclude the current user and filter by opposite gender
        potential_matches = UserDatabase.objects.exclude(username=username).filter(gender=opposite_gender)
        # Identify users who have any match requests with the current user
        users_with_match_requests = MatchRequest.objects.filter(
            Q(sender=current_user) | Q(receiver=current_user)
        ).values_list('sender', 'receiver')

        # Flatten the list of user IDs
        user_ids_with_match_requests = set()
        for sender_id, receiver_id in users_with_match_requests:
            user_ids_with_match_requests.add(sender_id)
            user_ids_with_match_requests.add(receiver_id)

        # Exclude users who have any match requests with the current user
        potential_matches = potential_matches.exclude(id__in=user_ids_with_match_requests)

        
         # Order by random and apply pagination
        potential_matches = potential_matches.order_by('?')[offset:offset + limit]
        

        # Fetch weights from the user preferences model
        weights = {
            'age': user_preferences.age_weight or 10,  # Use 10 as default if not specified
            'religion': user_preferences.religion_weight or 10,  # Use 10 as default if not specified
            'caste': user_preferences.caste_weight or 5,  # Use 5 as default if not specified
            'height': user_preferences.height_weight or 5,  # Optional: add height weight
            'weight': user_preferences.weight_weight or 5,  # Optional: add weight weight
            'gotra': user_preferences.gotra_weight or 10,  
            'habits': 5,  
        }

        # Preferences from the user preferences model
        preferences = {
            'age_min': user_preferences.p_age_min,
            'age_max': user_preferences.p_age_max,
            'religion': user_preferences.p_religion,
            'caste': user_preferences.p_caste,
            'gotra': user_preferences.p_gotra,
            'height_min': user_preferences.p_height_min,
            'height_max': user_preferences.p_height_max,
            'weight_min': user_preferences.p_weight_min,
            'weight_max': user_preferences.p_weight_max,
            'drinking': user_preferences.p_habits_drinking,
            'eating': user_preferences.p_habits_eating,
            'smoking': user_preferences.p_habits_smoking
        }


        matches = []
        for user in potential_matches:
            score = calculate_weighted_score(current_user, user, weights,preferences)
            matches.append({'username': user.username, 'score': score})

        # Sort matches by compatibility score (ascending order for best matches)
        sorted_matches = sorted(matches, key=lambda x: x['score'])

        # Return only the usernames
        return Response({"matches": [match['username'] for match in sorted_matches]}, status=status.HTTP_200_OK)
    





class SearchUserView(APIView):
    def get(self, request, *args, **kwargs):
        # Get query parameters with proper validation
        try:
            search_term = request.query_params.get('search', '')
            age_min = request.query_params.get('age_min', None)
            age_max = request.query_params.get('age_max', None)
            gender = request.query_params.get('gender', 'Any')
            religion = request.query_params.get('religion', 'Any')
            caste = request.query_params.get('caste', 'Any')
            gotra = request.query_params.get('gotra', 'Any')
            page_number = int(request.query_params.get('page', 1))
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construct the queryset based on the search term and filters
        users = UserDatabase.objects.all()

        if search_term:
            users = users.filter(
                Q(username__icontains=search_term) | Q(name__icontains=search_term)
            )

        # Apply filters if they are not 'Any'
        if gender != 'Any':
            users = users.filter(gender=gender)

        if religion != 'Any':
            users = users.filter(religion=religion)

        if caste != 'Any':
            users = users.filter(caste=caste)

        if gotra != 'Any':
            users = users.filter(gotra=gotra)

        if age_min is not None and age_max is not None:
            users = users.filter(age__gte=age_min, age__lte=age_max)

        users = users.order_by('id')  # Adjust ordering if needed

        # Paginate the queryset
        paginator = Paginator(users, 10)  # 10 users per page
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return Response(
                {"error": "Page number out of range."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create a custom response with only the necessary fields
        response_data = {
            "total_pages": paginator.num_pages,
            "current_page": page_number,
            "users": [
                {
                    "username": user.username,
                }
                for user in page_obj
            ]
        }

        # Return paginated data
        return Response(response_data, status=status.HTTP_200_OK)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserPreferences
from .serializers import UserPreferencesSerializer


class SaveUserPreferences(APIView):
    def post(self, request, *args, **kwargs):
        user = UserDatabase.objects.get(username=request.data['username'])  # Get user by username
        preferences_data = {
            'user': user,
            
            'p_age_min': request.data.get('p_age_min', None),
            'p_age_max': request.data.get('p_age_max', None),

            'p_religion': request.data.get('p_religion', None),

            
            'p_caste': request.data.get('p_caste', None),

            
            'p_gotra': request.data.get('p_gotra', None),

            'p_height_min': request.data.get('p_height_min', None),
            'p_height_max': request.data.get('p_height_max', None),

            
            'p_weight_min': request.data.get('p_weight_min', None),
            'p_weight_max': request.data.get('p_weight_max', None),

            'p_habits_drinking': request.data.get('p_habits_drinking', None),
            'p_habits_eating': request.data.get('p_habits_eating', None),
            'p_habits_smoking': request.data.get('p_habits_smoking', None),
        }
        
        preferences, created = UserPreferences.objects.update_or_create(
            user=user,
            defaults=preferences_data
        )
        
        if created:
            return Response({"message": "Preferences saved successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Preferences updated successfully!"}, status=status.HTTP_200_OK)


class SaveUserWeights(APIView):
    def post(self, request, *args, **kwargs):
        user = UserDatabase.objects.get(username=request.data['username'])  # Get user by username
        weight_data = {
            'user': user,
            'age_weight': request.data.get('age_weight', None),
            'religion_weight': request.data.get('religion_weight', None),
            'caste_weight': request.data.get('caste_weight', None),
            'gotra_weight': request.data.get('gotra_weight', None),
            'height_weight': request.data.get('height_weight', None),
            'weight_weight': request.data.get('weight_weight', None),

        }
        
        preferences, created = UserPreferences.objects.update_or_create(
            user=user,
            defaults=weight_data
        )
        
        if created:
            return Response({"message": "Weights saved successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Weights updated successfully!"}, status=status.HTTP_200_OK)
