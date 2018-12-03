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
        concepts = group.concept_set.all()
        amount = sum([c.current_amount_per_month for c in concepts])
        print(group, amount)
        if amount < 0:
            expenses.append([group, amount, concepts])
        else:
            incomes.append([group, amount, concepts])

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


