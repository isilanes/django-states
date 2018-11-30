# Django libs:
from django.db import models
from django.utils import timezone


# Classes:
class Concept(models.Model):
    name = models.CharField('Name', max_length=200)
    periodic = models.BooleanField("Periodic", default=False)

    # Public properties:
    @property
    def current_amount_per_day(self):
        """Euros per day in (positive) or out (negative), as of latest changes."""

        # For periodic concepts, take latest period:
        if self.periodic:
            try:
                prev, curr = list(self.updates)[-2:]
                dt = (curr.when - prev.when).total_seconds() / 86400.  # delta time in days
                return curr.amount / dt
            except ValueError:
                return 0.1

        return 0.0

    @property
    def updates(self):
        """List of Updates in this concept, sorted by date."""

        return Update.objects.filter(concept=self).order_by("when")

    @property
    def current_amount_per_month(self):
        """Euros per month in (positive) or out (negative), as of latest changes."""

        return self.current_amount_per_day * 30

    # Special methods:
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Update(models.Model):
    concept = models.ForeignKey(Concept, blank=True, on_delete=models.CASCADE, default=1)
    when = models.DateTimeField("When", blank=True, default=timezone.now)
    amount = models.FloatField("Amount", default=0.0)  # positive = income, negative = expense

    # Special methods:
    def __str__(self):
        return f"{self.amount} euros for '{self.concept}' on {self.when}"

