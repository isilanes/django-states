# Django libs:
from django.db import models
from django.utils import timezone

# Our libs:
from .managers import EventManager


# Classes:
class Expense(models.Model):
    concept = models.CharField('Concept', max_length=200)
    objects = EventManager()

    # Special methods:
    def __str__(self):
        return self.concept

    def __unicode__(self):
        return self.__str__()


class PeriodicExpense(Expense):
    frequency = models.FloatField("Frequency", default=30.0)


class OneOffExpense(Expense):

    # Public methods:
    pass

    # Public properties:


class Update(models.Model):
    expense = models.ForeignKey(Expense, blank=True, on_delete=models.CASCADE)
    when = models.DateTimeField("When", blank=True, default=timezone.now)
    sum = models.FloatField("Sum", default=0.0)

    # Special methods:
    def __str__(self):
        return f"{self.sum} euros for '{self.expense}' on {self.when}"


