# Django libs:
from django.contrib import admin

# Our libs:
from .models import PeriodicExpense, OneOffExpense, Update, SporadicExpense


# Classes:
class UpdateInline(admin.StackedInline):
    model = Update
    extra = 1


@admin.register(PeriodicExpense)
class PeriodicExpenseAdmin(admin.ModelAdmin):
    fields = ["concept", "frequency"]
    list_display = ("concept",)
    search_fields = ["concept"]
    inlines = [UpdateInline]


@admin.register(OneOffExpense)
class OneOffExpenseAdmin(admin.ModelAdmin):
    fields = ["concept"]
    list_display = ("concept",)
    search_fields = ["concept"]
    inlines = [UpdateInline]


@admin.register(SporadicExpense)
class SporadicExpenseAdmin(admin.ModelAdmin):
    fields = ["concept"]
    list_display = ("concept",)
    search_fields = ["concept"]
    inlines = [UpdateInline]


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    pass
