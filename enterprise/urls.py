from django.urls import path

from . import views

app_name = "enterprise"

urlpatterns = [
    path("", views.index, name="index"),
]
