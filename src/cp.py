#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from base.texts import ALERTS
from core.models import Qada  # Qazo Nomozlari Models


def main(request):
    result = {
        "app_name": settings.APP_NAME,
        'show_alert': request.session.get('show_alert', 'hidden'),

    }
    result.update({"alert": ALERTS})
    if not request.user.is_anonymous:
        # Get today's date
        today = timezone.now().date()

        # Calculate the first day of the current month
        first_day_of_month = today.replace(day=1)

        # Calculate the last day of the current month
        if today.month == 12:
            last_day_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

        # Get all dates in the current month that are already in the database
        existing_dates = Qada.objects.filter(user=request.user, date__range=(first_day_of_month, last_day_of_month)).values_list('date', flat=True)

        # Loop through all dates in the current month
        current_date = first_day_of_month
        while current_date <= last_day_of_month:
            # If the current date is not in the database, add it
            if current_date not in existing_dates:
                Qada.objects.create(date=current_date, user=request.user)  # replace with your actual create method
            # Go to the next date
            current_date += timedelta(days=1)

        result.update({
            "now_year": int(today.strftime('%Y')),
            "now_month": int(today.strftime('%m')),
        })

    return result


