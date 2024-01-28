from contextlib import closing
from datetime import datetime, timedelta, date

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from base.helper import from_date, formatter
from core.models import Qada
# Create your views here.
from dateutil.relativedelta import relativedelta


@login_required(login_url='login')
def index(request):
    current_date = datetime.now().date()
    todays = Qada.objects.get_or_create(user=request.user, date=current_date)[0]

    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)
    start = first_day_of_month.strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    # Get the QuerySet from the first day of the month until today
    sql = f"""
        SELECT date, bomdod, peshin, asr, shom , xufton , vitr 
        from core_qada 
        where user_id = 1
        and  "date" BETWEEN "{start}" and "{end}" 
        and (bomdod == 'bg-danger' or peshin == 'bg-danger' or asr == 'bg-danger' or shom == 'bg-danger' or xufton == 'bg-danger' or vitr == 'bg-danger')
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = formatter(cursor.fetchall())

    ctx = {
        "today": todays,

        'date_today': today,
        "now_year": int(today.strftime('%Y')),
        "now_month": int(today.strftime('%m')),
        "events": result

    }
    request.session['last_path'] = request.path
    return render(request, 'pages/index.html', ctx)


@login_required(login_url='login')
def grader(request, pk, status, type):
    last_path = request.session.get('last_path', '/')

    qada = Qada.objects.filter(id=pk).first()
    if not qada:
        return redirect('home')
    if status not in ['bg-warning', 'bg-success', 'bg-danger']:
        return redirect('home')
    sql = f"""
    update core_qada
    set {type} = "{status}"
    where id={pk}
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)

    return HttpResponseRedirect(last_path)


def goto(request):
    last_path = request.session.get('last_path', '/')
    year = int(request.GET.get('year', 0))
    month = int(request.GET.get('months', 1))
    if year < 1900:
        return redirect(last_path)

    return redirect('report', year=year, month=month)


@login_required(login_url='login')
def report(request, year, month):
    last_path = request.session.get('last_path', '/')
    start_date = date(year, month, 1)
    first_day_of_month = start_date.replace(day=1)

    # Get today's date
    now = datetime.now()
    today = now.date()
    if start_date > today or year < 1950:
        return redirect(last_path)
    # Get the previous month
    prev_month = start_date - relativedelta(months=1)

    # Check if the date object is the same as today's date
    if (start_date.year == today.year) and (start_date.month == today.month):
        queryset1 = Qada.objects.filter(user=request.user,
                                        date__range=(first_day_of_month, today)).order_by('-date')
        next_month = None

    else:
        if start_date.month == 12:
            last_day_of_month = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day_of_month = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)

        queryset1 = Qada.objects.filter(user=request.user,
                                        date__range=(first_day_of_month, last_day_of_month)).order_by('-date')
        # Get the next month
        next_month = start_date + relativedelta(months=1)

    if not queryset1:
        from_date(request, year, month)
        return redirect('report', year=year, month=month)

    ctx = {
        "report_monthly": queryset1,
        "info": start_date,
        "next": next_month,
        "prev_year": int(prev_month.strftime('%Y')),
        "prev": prev_month,
        "prev_month": int(prev_month.strftime('%m')),

        'today': today,
        "now_year": int(today.strftime('%Y')),
        "now_month": int(today.strftime('%m')),



    }
    if next_month:
        ctx.update({
            "next_year": int(next_month.strftime('%Y')),
            "next_month": int(next_month.strftime('%m')),
        })

    request.session['last_path'] = request.path
    return render(request, 'pages/report.html', ctx)


@login_required(login_url='login')
def qada_events(request):
    last_path = request.session.get('last_path', '/')

    year = int(request.GET.get('year', 1900))
    month = int(request.GET.get('month', 1))

    start_date = date(year, month, 1)
    now = datetime.now()
    today = now.date()

    if start_date > today or year < 1950:
        return JsonResponse({"events": []})

    if (start_date.year == today.year) and (start_date.month == today.month):
        last_day_of_month = today

    else:
        if start_date.month == 12:
            last_day_of_month = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day_of_month = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)

    start = start_date.strftime('%Y-%m-%d')
    end = last_day_of_month.strftime('%Y-%m-%d')

    # start_date = date(year, month, 1)
    # if start_date.month == 12:
    #     last_day_of_month = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
    # else:
    #     last_day_of_month = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)

    sql = f"""
    SELECT date, bomdod, peshin, asr, shom , xufton , vitr 
    from core_qada 
    where user_id = 1
    and  "date" BETWEEN "{start}" and "{end}" 
    and (bomdod == 'bg-danger' or peshin == 'bg-danger' or asr == 'bg-danger' or shom == 'bg-danger' or xufton == 'bg-danger' or vitr == 'bg-danger')
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = formatter(cursor.fetchall())

    print(result)

    return JsonResponse({"events": result})
