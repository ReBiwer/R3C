from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot
from robots.schemas import RobotInfo

from .services import send_availability_notifications


@receiver(post_save, sender=Robot)
def notify_customers_on_robot_available(sender: Robot.__class__, instance: Robot, created: bool, **kwargs):
    if created:
        robot_info = RobotInfo(serial=instance.serial, model=instance.model, version=instance.version)
        send_availability_notifications(robot_info)
