from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from pandas import DataFrame

from .models import Robot
from .schemas import RobotToExcel


def get_info_robots() -> list[RobotToExcel]:
    """Возвращает данные из БД валидированные pydantic схемой"""
    one_week_ago = timezone.now() - timedelta(days=7)
    robots = Robot.objects.filter(created__gte=one_week_ago).values("model", "version").annotate(total=Count("id"))
    result = [RobotToExcel.model_validate(robot_data) for robot_data in robots]
    return result


def get_dataframe(data: list[RobotToExcel]) -> DataFrame:
    """Преобразовывает информацию о роботах в DataFrame"""
    name_columns = {"model": "Модель", "version": "Версия", "total": "Количество за неделю"}
    data_robot = [robot.model_dump() for robot in data]
    df = DataFrame(data_robot)
    df.rename(columns=name_columns, inplace=True)
    return df
