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
        """Unordered list of all Concepts in Group."""

        positives = [c for c in self.concept_set.all() if c.current_amount_per_day >= 0]
        positives = [c for a, c in sorted([(c.current_amount_per_day, c) for c in positives], reverse=True)]

        negatives = [c for c in self.concept_set.all() if c.current_amount_per_day < 0]
        negatives = [c for a, c in sorted([(c.current_amount_per_day, c) for c in negatives])]

        return positives + negatives

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
    def current_amount_per_day(self):
        """Euros per day in (positive) or out (negative), as of latest changes."""

        # For periodic concepts, take latest period only:
        if self.periodic:
            try:
                current = list(self.updates)[-1]
                return current.amount / self.periodicity
            except ValueError:
                return 0.0
        # Non-periodic concepts are averaged over the latest up to 5:
        else:
            try:
                latest = list(self.updates)[-5:]
                total_sum = sum([x.amount for x in latest])
                dt = (timezone.now() - latest[0].when).total_seconds() / 86400.  # delta time in days
                return total_sum / dt
            except IndexError:
                return 0.0

    @property
    def updates(self):
        """List of Updates in this concept, sorted by date."""

        return self.update_set.order_by("when")

    @property
    def current_amount_per_month(self):
        """Euros per month in (positive) or out (negative), as of latest changes."""

        return self.current_amount_per_day * 30

    @property
    def periodicity(self):
        """Infer periodicity from all logged activity. Return in days."""

        u = list(self.updates)
        if len(u) < 2:
            return 30

        first = u[0]
        last = u[-1]
        days = (last.when - first.when).total_seconds() / 86400.

        return days / (len(u) - 1)

    # Special methods:
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Update(models.Model):
    concept = models.ForeignKey(Concept, blank=True, on_delete=models.CASCADE, default=1)
    when = models.DateTimeField("When", blank=True, default=timezone.now)
    amount = models.FloatField("Amount", default=0.0)  # positive = income, negative = expense
    comment = models.CharField("Comment", max_length=500, default=" ")

    # Special methods:
    def __str__(self):
        return f"{self.amount} euros for '{self.concept}' on {self.when}"


