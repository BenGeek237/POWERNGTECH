from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_password_reset_email(user):
    """
    Generate a password reset token and send an email to the user.
    """
    # 1. Generate token and uid
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    
    # 2. Build the password reset URL for the frontend
    # Example: http://localhost:5173/auth/reinitialisation/<uid>/<token>
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:5173")
    reset_url = f"{frontend_url.rstrip('/')}/auth/reinitialisation/{uidb64}/{token}"
    
    # 3. Create email content
    subject = "Réinitialisation de votre mot de passe - POWER NG TECHNOLOGIE"
    message = f"""Bonjour {user.first_name},

Vous avez demandé la réinitialisation de votre mot de passe sur POWER NG TECHNOLOGIE.

Veuillez cliquer sur le lien ci-dessous pour créer un nouveau mot de passe :
{reset_url}

Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email en toute sécurité. Le lien expirera automatiquement.

L'équipe POWER NG TECHNOLOGIE
"""
    
    # 4. Send email
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@powerngtech.com")
    send_mail(
        subject,
        message,
        from_email,
        [user.email],
        fail_silently=False,
    )
