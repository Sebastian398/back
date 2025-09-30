from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import PerfilUsuario

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    from django.conf import settings
    
    # Obtener información del usuario
    user = reset_password_token.user
    
    # Construir la URL completa para reset de contraseña
    reset_url = instance.request.build_absolute_uri(
        reverse('password_reset:reset-password-confirm')
    )
    
    # Contexto para el template
    context = {
        'current_user': user,
        'username': user.username,
        'first_name': user.first_name or user.username,
        'email': user.email,
        'reset_password_url': f"{reset_url}?token={reset_password_token.key}",
        'token': reset_password_token.key,  # Token explícito
        'domain': instance.request.get_host(),
        'site_name': 'PlantIQ - Sistema de Riego',
    }

    # Render templates para email
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    # Crear y enviar email
    msg = EmailMultiAlternatives(
        "Restablecimiento de Contraseña - PlantIQ",
        email_plaintext_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    
    try:
        msg.send()
        print(f"Email de reset enviado exitosamente a {user.email} con token: {reset_password_token.key}")
    except Exception as e:
        print(f"Error enviando email de reset: {str(e)}")

@receiver(post_save, sender=User)
def crear_o_guardar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)
    else:
        instance.perfilusuario.save()