from datetime import datetime
from utils import zero_time_and_set_day_to_1, increment_months
from model import train

first_of_current_month = zero_time_and_set_day_to_1(datetime.today())
initial_month = increment_months(first_of_current_month, -1)

data_key = "ip_address"

# TODO: How do we set data_key
train(initial_month, initial_month, data_key)