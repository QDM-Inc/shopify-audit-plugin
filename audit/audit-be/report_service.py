from datetime import datetime

import pytz

import sys

def get_total_sales(orders):
    sales = []
    if len(orders) >= 1:
        for item in orders:
            sales.append(float(orders[item]['total_price']))

        total = sum(sales)
        return round(total, 2)
    else:
        return 'No orders found'


def get_first_order_date(orders):
    dates = []

    for item in orders:
        # TODO: add fullfillment status on real store
        # if orders[item].fulfillment_status == 'fulfilled':
            dates.append(datetime.fromisoformat((orders[item]['created_at'])))

    dates.sort()
    return dates[0]


def convert_utc_to_local_time(utc_date):
    local_timezone = pytz.timezone('US/Eastern')
    local_date = utc_date.replace(tzinfo=pytz.utc)
    local_date = local_date.astimezone(local_timezone)
    return local_date

    
# check later with date-time
def convert_ISO_to_month(ISOdate):
    local_timezone = pytz.timezone('US/Eastern')
    local_date = ISOdate.replace(tzinfo=pytz.utc)
    local_date = local_date.astimezone(local_timezone)
    return local_date


def process_customers_data(data):
    for customer in data:
        if data[customer]['orders_count'] > 1:
            data[customer]['type'] = 'Returning'
        elif data[customer]['orders_count'] == 1:
            data[customer]['type'] = 'First-time'
        elif data[customer]['orders_count'] == 0:
            data[customer]['type'] = "Haven't ordered yet"
            data[customer]['recent_purchase'] = "Haven't ordered yet"
            data[customer]['first_purchase'] = "Haven't ordered yet"
            data[customer]['aov'] = 0

    return data

def get_order_dates_by_customer_id(orders):
  dict = {}
  for item in orders: 
    if orders[item]['total_price'] > 0:
      customerId = orders[item]['customer']['id']
      orderDates = datetime.fromisoformat((orders[item]['created_at']))
      if customerId in dict:
        dict[customerId] = [orderDates]
      else:
        dict[customerId].append(orderDates)
        dict[customerId].sort()  
    else: 
      return 'order price<0'
  return dict

