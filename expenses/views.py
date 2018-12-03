# Django libs:
from django.shortcuts import render, redirect

# Our libs:
from .models import Concept, Group


# Views:
def index(request):
    """Index view."""

    # Get all non one-off expenses/incomes:
    expenses, incomes = [], []
    for group in Group.objects.all():
        if group.net < 0:
            expenses.append(group)
        else:
            incomes.append(group)

    net = sum([c.current_amount_per_month for c in Concept.objects.all()])

    for concept in Concept.objects.filter(group=None):
        print(concept, "has no group!")

    # As always, build context:
    context = {
        "expenses": expenses,
        "incomes": incomes,
        "net": net,
    }

    return render(request, "expenses/index.html", context)


