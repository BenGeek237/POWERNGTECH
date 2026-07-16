"""
POWER NG TECHNOLOGIE — Accounts Views
REST API views for authentication and profile management.
"""
from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserDetailSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from .utils import send_password_reset_email

User = get_user_model()


@extend_schema(tags=["Authentification"])
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Returns access token, refresh token, and user data.
    """
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=["Authentification"])
class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Create a new user account.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens for immediate login after registration
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Compte créé avec succès.",
                "user": UserDetailSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Authentification"])
class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Blacklist the refresh token to invalidate the session.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Profil"])
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/profile/  — Retrieve current user profile
    PUT  /api/auth/profile/  — Update current user profile
    PATCH /api/auth/profile/ — Partial update
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserProfileUpdateSerializer
        return UserDetailSerializer


@extend_schema(tags=["Profil"])
class ChangePasswordView(APIView):
    """
    POST /api/auth/password-change/
    Change the current user's password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(
            {"message": "Mot de passe modifié avec succès."},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentification"])
class PasswordResetRequestView(APIView):
    """
    POST /api/auth/password-reset/
    Send a password reset email to the user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        # Always return success to prevent email enumeration
        try:
            user = User.objects.get(email=email, is_active=True)
            send_password_reset_email(user)
        except User.DoesNotExist:
            pass

        return Response(
            {
                "message": "Si un compte existe avec cet email, "
                           "vous recevrez un lien de réinitialisation."
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentification"])
class PasswordResetConfirmView(APIView):
    """
    POST /api/auth/password-reset/confirm/
    Confirm password reset with token and set new password.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        
        return Response(
            {"message": "Votre mot de passe a été réinitialisé avec succès."},
            status=status.HTTP_200_OK,
        )
