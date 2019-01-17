# Django libs:
from django.shortcuts import render

# Our libs:
from .models import Concept, Group, Update


# Views:
def index(request, verbose=False):
    """Index view."""

    for concept in Concept.objects.filter(group=None):
        print(concept, "has no group!")

    # As always, build context:
    context = {
        "expenses": expense_groups(),
        "incomes": income_groups(),
        "net": current_global_net(),
        "verbose": verbose,
    }

    return render(request, "expenses/index.html", context)


def index_verbose(request):
    return index(request, verbose=True)


def event_list(request, verbose=False):
    """Event list view."""

    # As always, build context:
    context = {
        "events": Update.objects.all(),
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
