import json

from django.db import transaction
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.generic import View
from pydantic import ValidationError

from .models import Robot
from .schemas import RobotInfo


class AddRobot(View):

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            data: dict = json.loads(request.body)
            robots = []
            for data in data.values():
                serial_robot = f"{data['model']}-{data['version']}"
                data_robot = RobotInfo(serial=serial_robot, model=data["model"], version=data["version"])
                robots.append(Robot(**data_robot.model_dump()))
            with transaction.atomic():
                Robot.objects.bulk_create(robots)
            return JsonResponse({"success": True}, status=200)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=403)


