# send welcome message to the registered users

from django.core.mail import send_mail
from django.conf import settings
from client.models import Client




def send_welcome_email(user, tenant_name):
    subject = 'Welcome to Our Platform!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    if user.is_superuser:
        # Message for superusers (e.g., clients)
        message = (
            f"Dear {user.first_name},\n\n"
            "Welcome to BEESKUL!\n\n"
            "We are thrilled to have you as our esteemed client. Thank you for choosing our platform to "
            "manage your school's operations. If you have any questions or need support, our team is here "
            "to assist you.\n\n"
            "Best regards,\n"
            "The beesoft Team"
        )
    else:
        # Message for regular staff members
        message = (
            f"Dear {user.first_name},\n\n"
            f"Welcome to {tenant_name}!\n\n"
            "We are excited to have you as part of our team. You have been successfully registered as a "
            f"{get_role_display(user)}.\n\n"
            "If you have any questions or need assistance, please feel free to reach out.\n\n"
            "Best regards,\n"
            "The School Management Team"
        )

    send_mail(subject, message, email_from, recipient_list)

def get_role_display(user):
    if user.is_admin:
        return "Administrator"
    elif user.is_principal:
        return "Principal"
    elif user.is_class_master:
        return "Class Master"
    elif user.is_admission:
        return "Admission Officer"
    elif user.is_exam:
        return "Examination Officer"
    elif user.is_account:
        return "Accountant Officer"
    else:
        return "Staff Member"