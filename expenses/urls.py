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
    path('verbose', views.index_verbose, name="index_verbose"),
    path('list', views.event_list, name="list"),
]
