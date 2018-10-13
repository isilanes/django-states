# Django libs:
from django.db import models
from django.utils import timezone

# Our libs:
from .managers import EventManager


# Classes:
class Author(models.Model):
    name = models.CharField('Name', max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField("Title", max_length=300)
    pages = models.IntegerField("Pages", default=1)
    year = models.IntegerField("Year", default=1)

    # Public methods:
    def mark_read(self):
        """Mark self as read."""

        end = BookEndEvent(book=self, when=timezone.now())
        end.save()

    def set_pages(self, pages=None):
        """Mark 'pages' as pages read. Do nothing if 'None'."""

        if pages is not None:
            event = PageUpdateEvent(book=self, when=timezone.now(), pages_read=pages)
            event.save()

    # Public properties:
    @property
    def events(self):
        """List of events regarding book, sorted by date."""

        return Event.objects.filter(book=self).order_by("when").select_subclasses()

    @property
    def is_currently_being_read(self):
        """Returns True if it is currently being read. False otherwise."""

        being_read = False
        for event in self.events:
            if isinstance(event, BookStartEvent):
                being_read = True
            elif isinstance(event, BookEndEvent):
                being_read = False

        return being_read

    @property
    def is_already_read(self):
        """Returns True if it is already read. False otherwise."""

        read = False
        for event in self.events:
            if isinstance(event, BookStartEvent):
                read = False
            elif isinstance(event, BookEndEvent):
                read = True

        return read

    @property
    def pages_read(self):

        pages = 0
        for event in self.events:
            pages = event.page_equivalent

        return pages

    @property
    def date_read(self):
        """Return date of most recent time we finished reading it. None if never."""

        try:
            return BookEndEvent.objects.filter(book=self).order_by("-when")[0].when
        except IndexError:
            return None

    # Special properties:
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()


class Event(models.Model):
    book = models.ForeignKey(Book, blank=True, on_delete=models.CASCADE)
    when = models.DateTimeField("When", blank=True, default=timezone.now)
    objects = EventManager()


class PageUpdateEvent(Event):
    """The event of updating the pages of a book I have already read."""

    pages_read = models.IntegerField("Pages read", default=0)

    # Public properties:
    @property
    def page_equivalent(self):
        return self.pages_read

    # Special methods:
    def __str__(self):
        return f"{self.pages_read} pages read on '{self.book}'"

    def __unicode__(self):
        return self.__str__()


class BookStartEvent(Event):
    """The event of starting reading a book."""

    # Class properties:
    page_equivalent = 0

    # Special methods:
    def __str__(self):
        return f"'{self.book}' started"

    def __unicode__(self):
        return self.__str__()


class BookEndEvent(Event):
    """The event of finishing reading a book."""

    # Public properties:
    @property
    def page_equivalent(self):
        return self.book.pages

    # Special methods:
    def __str__(self):
        return f"'{self.book}' finished"

    def __unicode__(self):
        return self.__str__()


