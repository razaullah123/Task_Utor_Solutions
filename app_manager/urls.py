from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import AppViewSet, PlanViewSet, SubscriptionViewSet, UserSignUpView, PasswordResetView

router = DefaultRouter()
router.register(r'apps', AppViewSet, basename='apps')
router.register(r'plans', PlanViewSet, basename='plans')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('password_reset/', PasswordResetView.as_view(), name="password-reset"),
]

urlpatterns += router.urls