from django.urls import path

from .views import AddRobot
from .views import ExportToExcel

app_name = "robots"

urlpatterns = [path("add/", AddRobot.as_view(), name="add"), path("export/", ExportToExcel.as_view(), name="export")]
