from datetime import datetime
from utils import zero_time_and_set_day_to_1, increment_months
from model import train

# extract a string representing the date of the first of the previous month
first_of_current_month = zero_time_and_set_day_to_1(datetime.today())
previous_month = increment_months(first_of_current_month, -1)
previous_month_string = datetime.strftime(previous_month, "%Y-%m-%d")

# train a model on the last month of data
train(previous_month_string, previous_month_string)