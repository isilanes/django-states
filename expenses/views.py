# Django libs:
from django.shortcuts import render, redirect

# Bokeh libs:
from bokeh.plotting import figure
from bokeh.embed import components

# Our libs:
#from .forms import BookForm
from .models import Expense


# Views:
def index(request):
    """Index view."""

    context = {
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


