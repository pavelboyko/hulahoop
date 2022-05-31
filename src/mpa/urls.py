from django.urls import path
from mpa import views

urlpatterns = [
    path("", views.index, name="index"),
]
