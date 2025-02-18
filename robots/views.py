import json
from io import BytesIO

import pandas
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from pydantic import ValidationError

from .models import Robot
from .schemas import RobotInfo
from .utils import get_dataframe, get_info_robots


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

class ExportToExcel(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        output_file = BytesIO()
        robots = get_info_robots()
        df = get_dataframe(robots)
        with pandas.ExcelWriter(output_file, engine="openpyxl") as writer:
            for model, group in df.groupby("Модель"):
                group.to_excel(
                    writer,
                    sheet_name=str(model),
                    index=False,
                    columns=["Модель", "Версия", "Количество за неделю"]
                )
        output_file.seek(0)
        response = HttpResponse(output_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=robots_by_models.xlsx'
        return response
