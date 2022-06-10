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
        if customer['orders_count'] > 1:
            customer['type'] = 'Returning'
        elif customer['orders_count'] == 1:
            customer['type'] = 'First-time'
        elif customer['orders_count'] == 0:
            customer['type'] = "Haven't ordered yet"
            customer['recent_purchase'] = "Haven't ordered yet"
            customer['first_purchase'] = "Haven't ordered yet"
            customer['aov'] = 0

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


def group_orders_by_customer_id(orders):
  dict = {}
  for item in orders:
    customerId = orders[item]['customer']['id']
    if customerId in dict:
      dict[customerId] = [
        { "id": orders[item]['id'], "created_at": (orders[item]['created_at']) }]
    else: 
      dict[customerId].append({
        "id": orders[item]['id'],
        "created_at": orders[item]['created_at'],
      })
      dict[customerId].sort(key=lambda x: x['created_at'])
    
  
  return dict


def get_previous_order_date_by_order_id (ordersObj, orderId):
  for item in ordersObj:
    if len(ordersObj[item]) > 1:
      for i in range(len(ordersObj[item])-1, -1, -1):
        if ordersObj[item][i]['id'] == orderId:
          return ordersObj[item][i - 1]['created_at']

