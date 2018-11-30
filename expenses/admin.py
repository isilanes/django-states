# Django libs:
from django.contrib import admin

# Our libs:
from .models import Concept, Update


# Classes:
class UpdateInline(admin.StackedInline):
    model = Update
    extra = 1


@admin.register(Concept)
class PeriodicExpenseAdmin(admin.ModelAdmin):
    fields = ["name", "periodic"]
    list_display = ("name",)
    search_fields = ["name"]
    inlines = [UpdateInline]


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    pass


