# Django libs:
from django.contrib import admin

# Our libs:
from .models import Author, Book, PageUpdateEvent, BookStartEvent, BookEndEvent


# Classes:
class PageUpdateInline(admin.StackedInline):
    model = PageUpdateEvent
    extra = 0


class BookStartInline(admin.StackedInline):
    model = BookStartEvent
    extra = 0


class BookEndInline(admin.StackedInline):
    model = BookEndEvent
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ["title", "authors", "pages", "year"]
    list_display = ("title", "year")
    search_fields = ["title"]
    inlines = [BookStartInline, PageUpdateInline, BookEndInline]


@admin.register(BookStartEvent)
class BookStartEventAdmin(admin.ModelAdmin):
    pass


@admin.register(PageUpdateEvent)
class PageUpdateEventAdmin(admin.ModelAdmin):
    pass


@admin.register(BookEndEvent)
class BookEndEventAdmin(admin.ModelAdmin):
    pass
