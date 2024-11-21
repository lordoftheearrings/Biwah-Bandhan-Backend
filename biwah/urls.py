from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UserProfileUpdateView, UserLoginView, UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user-profile/<str:username>/', UserProfileUpdateView.as_view(), name='user-profile'),
    path('update-profile/<str:username>/', UserProfileUpdateView.as_view(), name='update-profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)