# Django libs:
from django.shortcuts import render

# Our libs:
from .models import Concept, Group, OneOffUpdate, Update, PeriodicUpdate


# Views:
def index(request):
    """Index view."""

    for concept in Concept.objects.filter(group=None):
        print(concept, "has no group!")

    # As always, build context:
    context = {
        "expenses": expense_groups(),
        "incomes": income_groups(),
        "net": current_global_net(),
        "accumulated": current_global_accumulated(),
    }

    return render(request, "expenses/index.html", context)


def event_list(request):
    """Event list view."""

    # As always, build context:
    context = {
        "events": Update.objects.all().order_by("-when"),
    }

    return render(request, "expenses/event_list.html", context)


# Auxiliary functions:
def income_groups():
    """List of Groups with positive net amount, sorted by decreasing net amount."""

    return sorted([g for g in Group.objects.all() if g.net >= 0], reverse=True)


def expense_groups():
    """List of Groups with negative net amount, sorted by increasing net amount."""

    return sorted([g for g in Group.objects.all() if g.net < 0])


def current_global_net():
    """Current global monthly net."""

    return sum([c.current_amount_per_month for c in Concept.objects.all()])


def current_global_accumulated():
    """Current global accumulated total."""
    
    return sum([u.amount for u in PeriodicUpdate.objects.all()]) + sum([u.amount for u in OneOffUpdate.objects.all()])
