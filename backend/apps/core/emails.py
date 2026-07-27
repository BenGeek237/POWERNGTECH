"""
POWER NG TECHNOLOGIE — Utilitaires d'e-mail
Gère l'envoi d'e-mails en arrière-plan.
"""
import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        text_content = strip_tags(self.html_content)
        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.recipient_list
        )
        msg.attach_alternative(self.html_content, "text/html")
        msg.send(fail_silently=True)


def send_async_email(subject, template_name, context, recipient_list):
    """
    Renders an HTML template and sends it in a separate thread.
    """
    html_content = render_to_string(template_name, context)
    EmailThread(subject, html_content, recipient_list).start()
