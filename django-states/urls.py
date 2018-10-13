# Django libs:
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


# URL patterns:
urlpatterns = [
    # Admin view:
    path('admin/', admin.site.urls),

    # Main:
    path('', TemplateView.as_view(template_name="main_index.html"), name="main_index"),

    # Apps:
    path('gastos/', include('gastos.urls', namespace="gastos")),
]
