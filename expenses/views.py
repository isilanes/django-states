# Django libs:
from django.shortcuts import render, redirect

# Our libs:
from .models import Concept


# Views:
def index(request):
    """Index view."""

    # Get all non one-off expenses/incomes:
    expenses = [c for c in Concept.objects.all() if c.current_amount_per_day < 0]
    incomes = [c for c in Concept.objects.all() if c.current_amount_per_day >= 0]
    net = sum([c.current_amount_per_month for c in Concept.objects.all()])

    # As always, build context:
    context = {
        "expenses": expenses,
        "incomes": incomes,
        "net": net,
    }

    return render(request, "expenses/index.html", context)


