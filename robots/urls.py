from django.urls import path
from views import AddRobot

app_name = "robots"

urlpatterns = [
    path("add/", AddRobot.as_view(), name="add_robot"),
]
