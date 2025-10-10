import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', 'tu_email@gmail.com')
        self.smtp_password = os.getenv('SMTP_PASSWORD', 'tu_app_password')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)

    def send_password_reset_email(self, to_email, username, reset_token):
        """Enviar email de recuperación de contraseña"""
        try:
            # URL del frontend para reset de contraseña
            frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
            reset_url = f"{frontend_url}/reset-password?token={reset_token}"
            
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Recuperación de contraseña - Tienda Online'
            msg['From'] = self.from_email
            msg['To'] = to_email

            # Contenido en texto plano
            text_content = f"""
Hola {username},

Has solicitado recuperar tu contraseña. Para crear una nueva contraseña, haz clic en el siguiente enlace:

{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email.

Saludos,
Equipo de Tienda Online
            """

            # Contenido HTML
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Recuperación de contraseña</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f8f9fa; }}
        .button {{ display: inline-block; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Recuperación de contraseña</h1>
        </div>
        <div class="content">
            <p>Hola <strong>{username}</strong>,</p>
            <p>Has solicitado recuperar tu contraseña. Para crear una nueva contraseña, haz clic en el siguiente botón:</p>
            <p style="text-align: center;">
                <a href="{reset_url}" class="button">Restablecer contraseña</a>
            </p>
            <p>O copia y pega este enlace en tu navegador:</p>
            <p style="word-break: break-all; background-color: #e9ecef; padding: 10px; border-radius: 3px;">{reset_url}</p>
            <p><strong>Este enlace expirará en 24 horas.</strong></p>
            <p>Si no solicitaste este cambio, puedes ignorar este email.</p>
        </div>
        <div class="footer">
            <p>Saludos,<br>Equipo de Tienda Online</p>
        </div>
    </div>
</body>
</html>
            """

            # Adjuntar contenido
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)

            # Verificar si las credenciales son válidas
            if not self.smtp_username or not self.smtp_password or self.smtp_username == "tu_email@gmail.com":
                print(f"📧 EMAIL SIMULADO para {to_email}:")
                print(f"🔗 Enlace de recuperación: {reset_url}")
                print(f"⏰ Token expira en 24 horas")
                return True

            # Enviar email real
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            print(f"Email de recuperación enviado a {to_email}")
            return True

        except Exception as e:
            print(f"Error enviando email a {to_email}: {str(e)}")
            return False

    def send_welcome_email(self, to_email, username):
        """Enviar email de bienvenida"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Bienvenido a Tienda Online'
            msg['From'] = self.from_email
            msg['To'] = to_email

            text_content = f"""
Hola {username},

¡Bienvenido a Infinite Finds!

Tu cuenta ha sido creada exitosamente. Ahora puedes:

- Explorar nuestros productos
- Realizar compras
- Gestionar tu perfil
- Contactar soporte

¡Gracias por unirte a nosotros!

Saludos,
Equipo de Infinite Finds
            """

            text_part = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(text_part)

            if not self.smtp_username or not self.smtp_password:
                print(f"SMTP no configurado. Email de bienvenida simulado para {to_email}")
                return True

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            print(f"Email de bienvenida enviado a {to_email}")
            return True

        except Exception as e:
            print(f"Error enviando email de bienvenida a {to_email}: {str(e)}")
            return False
