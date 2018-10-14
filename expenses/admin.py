# Django libs:
from django.contrib import admin

# Our libs:
from .models import PeriodicExpense, OneOffExpense, Update, SporadicExpense
from .models import PeriodicIncome, OneOffIncome, IncomeUpdate, SporadicIncome


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


class IncomeUpdateInline(admin.StackedInline):
    model = IncomeUpdate
    extra = 1


@admin.register(PeriodicIncome)
class PeriodicIncomeAdmin(admin.ModelAdmin):
    fields = ["concept", "frequency"]
    list_display = ("concept",)
    search_fields = ["concept"]
    inlines = [IncomeUpdateInline]


@admin.register(OneOffIncome)
class OneOffIncomeAdmin(admin.ModelAdmin):
    fields = ["concept"]
    list_display = ("concept",)
    search_fields = ["concept"]
    inlines = [IncomeUpdateInline]


@admin.register(SporadicIncome)
class SporadicIncomeAdmin(admin.ModelAdmin):
    fields = ["concept"]
    list_display = ("concept",)
    search_fields = ["concept"]
    inlines = [IncomeUpdateInline]


@admin.register(IncomeUpdate)
class IncomeUpdateAdmin(admin.ModelAdmin):
    pass
