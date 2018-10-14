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
    """Expenses that happen with a fixed periodicity."""

    frequency = models.FloatField("Frequency", default=30.0)

    # Public properties:
    @property
    def current_amount(self):
        """Value (euros) of current state of expense. Latest value."""

        return Update.objects.filter(expense=self).order_by("-when").first().sum

    @property
    def monthly_cost(self):
        """Equivalent monthly cost."""

        return 30.0 * self.current_amount / self.frequency


class OneOffExpense(Expense):
    """These expenses are not recurring, so do not take them into account, actually."""

    # Public properties:
    @property
    def current_amount(self):
        """One-off expenses incur in no recurring cost."""

        return 0.0

    @property
    def monthly_cost(self):
        """One-off expenses incur in no recurring cost."""

        return 0.0


class SporadicExpense(Expense):
    """These expenses happen at irregular intervals."""

    # Public properties:
    @property
    def monthly_cost(self):
        """Sum all historic expenses, and divide by months between first expense and now."""

        updates = Update.objects.filter(expense=self)
        s = sum([u.sum for u in updates]) # euros
        dt = (timezone.now() - updates.order_by("when").first().when).days / 30.0 # months

        return s / dt


class Income(models.Model):
    concept = models.CharField('Concept', max_length=200)
    objects = EventManager()

    # Special methods:
    def __str__(self):
        return self.concept

    def __unicode__(self):
        return self.__str__()


class PeriodicIncome(Income):
    """Incomes that happen with a fixed periodicity."""

    frequency = models.FloatField("Frequency", default=30.0)

    # Public properties:
    @property
    def current_amount(self):
        """Value (euros) of current state of income. Latest value."""

        return IncomeUpdate.objects.filter(income=self).order_by("-when").first().sum

    @property
    def monthly_amount(self):
        """Equivalent monthly amount."""

        return 30.0 * self.current_amount / self.frequency


class OneOffIncome(Income):
    """These incomes are not recurring, so do not take them into account, actually."""

    # Public properties:
    @property
    def current_amount(self):
        """One-off incomes produce no recurring income."""

        return 0.0

    @property
    def monthly_amount(self):
        """One-off incomes produce no recurring income."""

        return 0.0


class SporadicIncome(Income):
    """These incomes happen at irregular intervals."""

    # Public properties:
    @property
    def monthly_amount(self):
        """Sum all historic incomes, and divide by months between first income and now."""

        updates = IncomeUpdate.objects.filter(income=self)
        s = sum([u.sum for u in updates]) # euros
        dt = (timezone.now() - updates.order_by("when").first().when).days / 30.0 # months

        return s / dt


class Update(models.Model):
    expense = models.ForeignKey(Expense, blank=True, on_delete=models.CASCADE)
    when = models.DateTimeField("When", blank=True, default=timezone.now)
    sum = models.FloatField("Sum", default=0.0)

    # Special methods:
    def __str__(self):
        return f"{self.sum} euros for '{self.expense}' on {self.when}"


class IncomeUpdate(models.Model):
    income = models.ForeignKey(Income, blank=True, on_delete=models.CASCADE)
    when = models.DateTimeField("When", blank=True, default=timezone.now)
    sum = models.FloatField("Sum", default=0.0)

    # Special methods:
    def __str__(self):
        return f"{self.sum} euros for '{self.income}' on {self.when}"


