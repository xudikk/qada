from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Qada
# Create your views here.


def calculator():
    # Get today's date
    today = datetime.now().date()

    # Calculate the first day of the current month
    first_day_of_month = today.replace(day=1)

    # Calculate the last day of the current month
    if today.month == 12:
        last_day_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

    # Get the QuerySet from the first day of the month until today
    queryset1 = Qada.objects.filter(date__range=(first_day_of_month, today)).order_by('-date')

    # Get the QuerySet from today to the last day of the month
    queryset2 = Qada.objects.filter(date__range=(today, last_day_of_month)).order_by('-date')

    return {
        "to_now": queryset1,
        "from_now": queryset2
    }


@login_required(login_url='login')
def index(request):
    current_date = datetime.now().date()
    today = Qada.objects.get_or_create(user=request.user, date=current_date)[0]
    all = Qada.objects.all().order_by('-date')

    ctx = {
        "today": today,
        "all": all
    }
    ctx.update(calculator())

    return render(request, 'pages/index.html', ctx)


@login_required(login_url='login')
def grader(request):
    pass