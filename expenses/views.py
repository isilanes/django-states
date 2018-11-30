# Django libs:
from django.shortcuts import render, redirect

# Our libs:
from .models import Concept


# Views:
def index(request):
    """Index view."""

    # Get all non one-off expenses/incomes:
    concepts = Concept.objects.all()

    # As always, build context:
    context = {
        "expenses": concepts,
        "incomes": [],
        "net": 0.0,
    }

    return render(request, "expenses/index.html", context)


