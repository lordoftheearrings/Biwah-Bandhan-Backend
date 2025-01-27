from django.contrib import admin
from .models import UserDatabase


class UserDatabaseAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'username', 
        'phone_number', 
        'age', 
        'gender', 
        'religion', 
        'caste',
        'name'
    )
    
    # Fields to search in the admin panel
    search_fields = ('username', 'phone_number', 'name', 'religion', 'caste')
    
    # Filters for easier navigation
    list_filter = ('gender', 'religion', 'caste')
    
    # Grouping fields in the admin edit page
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'password', 'phone_number', 'name', 'bio')
        }),
        ('Profile Images', {
            'fields': ('profile_image', 'cover_image')
        }),
        ('Demographic Information', {
            'fields': ('age', 'gender', 'religion', 'caste')
        }),
        ('Kundali Details', {
            'fields': (
                'birth_year', 'birth_month', 'birth_date',
                'birth_hour', 'birth_minute', 'birth_second',
                'birth_location', 'birth_latitude', 'birth_longitude', 
                'kundali_svg'
            )
        }),
    )

    # Making some fields read-only
    readonly_fields = ('kundali_svg',)

    # Enabling save as new feature
    save_as = True


# Register the model and admin configuration
admin.site.register(UserDatabase, UserDatabaseAdmin)
