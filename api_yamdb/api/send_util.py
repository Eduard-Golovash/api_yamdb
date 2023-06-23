from django.core.mail import send_mail


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Код подтверждения',
        message=f'Твой код подтверждения: {confirmation_code}',
        from_email='confirmation@ymail.ru',
        recipient_list=[email]
    )
