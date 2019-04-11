# Standard libs:
from datetime import timedelta

# Django libs:
from django.db import models
from django.utils import timezone


# Classes:
class Group(models.Model):
    name = models.CharField("Name", max_length=200)

    # Public properties:
    @property
    def net(self):
        """Monthly net amount of all Concepts in this Group."""

        return sum([c.current_amount_per_month for c in self.concepts])

    @property
    def concepts(self):
        """Ordered list of all Concepts in Group."""

        return sorted(self.concept_set.all())

    # Special methods:
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.net < other.net


class Concept(models.Model):
    name = models.CharField('Name', max_length=200)
    periodic = models.BooleanField("Periodic", default=False)
    group = models.ForeignKey(Group, blank=True, on_delete=models.CASCADE, null=True, default=1)

    # Public properties:
    @property
    def updates(self):
        """List of Updates in this concept, sorted by date."""

        return self.periodicupdate_set.order_by("when")

    @property
    def current_amount_per_month(self):
        """Euros per month in (positive) or out (negative), as of latest changes."""
        
        one_year_ago = timezone.now() - timedelta(days=365)
        
        last_year_updates = self.periodicupdate_set.filter(when__gt=one_year_ago)
        amount_in_a_year = sum([x.amount for x in last_year_updates])
        
        return amount_in_a_year / 12.

    @property
    def periodicity(self):
        """Infer periodicity from all logged activity. Return in days."""

        u = list(self.updates)
        if len(u) < 2:
            return None

        first = u[0]
        last = u[-1]
        days = (last.when - first.when).total_seconds() / 86400.

        return days / (len(u) - 1)

    # Special methods:
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

    def __lt__(self, other):
        if self.current_amount_per_month < 0 and other.current_amount_per_month < 0:
            return self.current_amount_per_month < other.current_amount_per_month

        return self.current_amount_per_month > other.current_amount_per_month


class Update(models.Model):
    """Base class for updates."""
    
    when = models.DateTimeField("When", blank=True, default=timezone.now)
    amount = models.FloatField("Amount", default=0.0)  # positive = income, negative = expense
    comment = models.CharField("Comment", max_length=500, default="-", blank=True)
    
    # Special methods:
    def __str__(self):
        return f"{self.amount} euros on {self.when}"
    
    # Properties
    def concept_name(self):
        try:
            return self.periodicupdate.concept.name
        except Update.DoesNotExist:
            return ""


class PeriodicUpdate(Update):
    """Periodic updates."""
    
    concept = models.ForeignKey(Concept, blank=True, on_delete=models.CASCADE, default=1)
    
    # Special methods:
    def __str__(self):
        return f"{self.amount} euros for '{self.concept}' on {self.when}"
    
    
class OneOffUpdate(Update):
    """One-off updates."""
    pass
