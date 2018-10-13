# Django libs:
from django.urls import path

# Our libs:
from . import views


# Constants:
app_name = "expenses"


# URL patterns:
urlpatterns = [
    # Main:
    path('', views.index, name="index"),
]
