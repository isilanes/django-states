# Django libs:
from django.contrib import admin

# Our libs:
from .models import Concept, Group, OneOffUpdate, PeriodicUpdate, DescriptionTranslation


# Classes:
class UpdateInline(admin.StackedInline):
    model = PeriodicUpdate
    extra = 1


@admin.register(Concept)
class PeriodicExpenseAdmin(admin.ModelAdmin):
    fields = ["name", "group", "periodic"]
    list_display = ("name",)
    search_fields = ["name"]
    inlines = [UpdateInline]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(OneOffUpdate)
class OneOffUpdateAdmin(admin.ModelAdmin):
    pass


@admin.register(PeriodicUpdate)
class PeriodicUpdateAdmin(admin.ModelAdmin):
    pass


@admin.register(DescriptionTranslation)
class DescriptionTranslationAdmin(admin.ModelAdmin):
    pass
