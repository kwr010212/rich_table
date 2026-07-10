from django.urls import path

from . import views

app_name = "survey"

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "register/complete/",
        views.register_complete,
        name="register_complete",
    ),
    path("enter/", views.enter, name="enter"),
]