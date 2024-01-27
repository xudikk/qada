#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from datetime import timedelta, date
from django.utils import timezone
from core.models import Qada


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

