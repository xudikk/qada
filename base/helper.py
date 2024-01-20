#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from datetime import timedelta, date
from django.utils import timezone
from core.models import Qada


def prev_month(request):
    if not request.user.is_anonymous:
        # Get today's date
        today = timezone.now().date()

        # Calculate the first day of the previous month
        if today.month == 1:
            first_day_of_prev_month = today.replace(year=today.year - 1, month=12, day=1)
        else:
            first_day_of_prev_month = today.replace(month=today.month - 1, day=1)

        # Calculate the last day of the previous month
        last_day_of_prev_month = today.replace(day=1) - timedelta(days=1)

        # Get all dates in the previous month that are already in the database
        existing_dates = Qada.objects.filter(user=request.user,
                                             date__range=(first_day_of_prev_month,
                                                          last_day_of_prev_month)).values_list('date', flat=True)

        # Loop through all dates in the previous month
        current_date = first_day_of_prev_month
        while current_date <= last_day_of_prev_month:
            # If the current date is not in the database, add it
            if current_date not in existing_dates:
                Qada.objects.create(user=request.user, date=current_date)
            # Go to the next date
            current_date += timedelta(days=1)


def from_date(request, year, month, day=1):
    # Get today's date
    today = timezone.now().date()

    # Set the start date
    start_date = date(year, month, day)

    # Get all dates from the start date to today that are already in the database
    existing_dates = Qada.objects.filter(user=request.user, date__range=(start_date, today)).values_list('date', flat=True)

    current_date = start_date
    while current_date <= today:
        if current_date not in existing_dates:
            Qada.objects.create(user=request.user, date=current_date)
        # Go to the next date
        current_date += timedelta(days=1)

