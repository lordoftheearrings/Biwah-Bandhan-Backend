from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserProfileUpdateView,
    UserProfileUpdateView2,
    UserLoginView,
    UserRegisterView,
    MatchmakingView,
)
from .kundali_views import GenerateKundaliView,RetrieveKundali
from .guna_milan_views import AshtakootGunMilan

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user-profile/<str:username>/', UserProfileUpdateView.as_view(), name='user-profile'),
    path('update-profile/<str:username>/', UserProfileUpdateView2.as_view(), name='update-profile'),
    path('weighted_score/<str:username>/', MatchmakingView.as_view(), name='weighted_score'),  
    path('generate_kundali/', GenerateKundaliView.as_view(), name='generate_kundali'),
    path('retrieve_kundali/',RetrieveKundali.as_view(),name='retrieve_kundali'),
    path('ashtakoot/', AshtakootGunMilan.as_view(), name='ashtakoot'),  
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
