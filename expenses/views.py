# Django libs:
from django.shortcuts import render, redirect

# Our libs:
from .models import Expense, OneOffExpense, Income, OneOffIncome


# Views:
def index(request):
    """Index view."""

    # Get all non one-off expenses/incomes:
    expenses = [e for e in Expense.objects.all().select_subclasses() if not isinstance(e, OneOffExpense)]
    incomes = [i for i in Income.objects.all().select_subclasses() if not isinstance(i, OneOffIncome)]
    net = net_monthly_saving()

    # As always, build context:
    context = {
        "expenses": expenses,
        "incomes": incomes,
        "net": net,
    }

    return render(request, "expenses/index.html", context)


def expense_detail(request, expense_id):
    """Detail view for a Expense."""

    expense = Expense.objects.get(pk=expense_id)

    context = {
        "expense": expense,
     }

    return render(request, "expense/expense_detail.html", context)


def modify_expense(request, expense_id):
    """Form to modify state of book."""

    expense = Expense.objects.get(pk=expense_id)

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book.set_pages(form.cleaned_data.get("pages_read"))
            return redirect("books:book_detail", book_id=book_id)

    else:
        initial = {
            "pages_read": book.pages_read,
        }
        form = BookForm(initial=initial)

    context = {
        "form": form,
        "book": book,
    }

    return render(request, 'books/modify_book.html', context)


# Helper functions:
def net_monthly_saving():
    """Net amount of money saved each month."""

    total = 0.0
    for expense in Expense.objects.all().select_subclasses():
        total -= expense.monthly_cost

    for income in Income.objects.all().select_subclasses():
        total += income.monthly_amount

    return total


