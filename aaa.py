#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan


from datetime import datetime, timedelta

# Number of days to add
days_to_add = 254

# Get the current date
current_date = datetime.now().date()

# Calculate the new date
new_date = current_date + timedelta(days=days_to_add)

print(f"The date after {days_to_add} days will be: {new_date}")





# Get today's date
today = datetime.now().date()

# Calculate the first day of the current month
first_day_of_month = today.replace(day=1)

# Calculate the last day of the current month
if today.month == 12:
    last_day_of_month = today.replace(year=today.year+1, month=1, day=1) - timedelta(days=1)
else:
    last_day_of_month = today.replace(month=today.month+1, day=1) - timedelta(days=1)

# Print the date ranges
print(f"From the first day of the month until today: {first_day_of_month} to {today}")
print(f"From today to the last day of the month: {today} to {last_day_of_month}")
