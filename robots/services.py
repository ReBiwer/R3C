import os
import dotenv

from django.core.mail import send_mail
from orders.models import Order
from robots.schemas import RobotInfo

dotenv.load_dotenv()

def send_availability_notifications(robot: RobotInfo):
    """Обработчик отправляющий уведомления на почту клиента"""
    orders = (
        Order.objects
        .select_related("customer")
        .filter(robot_serial=robot.serial)
    )
    email_subject = "Робот теперь в наличии"
    email_message = (
        f"Добрый день!\n"
        f"Недавно вы интересовались нашим роботом модели {robot.model}, версии {robot.version}.\n"
        f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
    )

    for order in orders:
        send_mail(
            email_subject,
            email_message,
            os.environ.get("DEFAULT_FROM_EMAIL"),
            [order.customer.email],
            fail_silently=False,
        )
