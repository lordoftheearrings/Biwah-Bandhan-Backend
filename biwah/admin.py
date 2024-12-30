from django.contrib import admin
from .models import User,Profile,Kundali


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)  # Display the username in the list view
    search_fields = ('username',)  # Allow search by username

admin.site.register(User, UserAdmin)

# Register Profile model with a custom admin class for better display
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'age', 'gender', 'religion', 'caste', 'bio', 'name')  # Customize the fields to display
    search_fields = ('user__username',)  # Allow search by user's username
    list_filter = ('gender', 'religion')  # Add filters by gender and religion

admin.site.register(Profile, ProfileAdmin)

# Register Kundali model with a custom admin class
class KundaliAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_year', 'birth_month', 'birth_date', 'birth_location')  # Customize the fields to display
    search_fields = ('user__username',)  # Allow search by user's username
    list_filter = ('birth_location',)  # Add filter by birth location

admin.site.register(Kundali, KundaliAdmin)