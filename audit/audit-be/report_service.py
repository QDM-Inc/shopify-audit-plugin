from datetime import datetime
from pprint import pprint
import time

import pytz

def get_total_sales(orders):
    sales = []
    if len(orders) >= 1:
        for item in orders:
            sales.append(item["total_price"])
        total = sum(sales)
        return round(total, 2)
    else:
        return 'No orders found'





def convert_utc_to_local_time(utc_date):
    local_timezone = pytz.timezone('US/Eastern')
    utc_date= str(utc_date)
    date_time_obj = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S%z")
    local_date = date_time_obj.replace(tzinfo=pytz.utc)
    local_date = local_date.astimezone(local_timezone)
    return local_date


def get_first_order_date(orders):
    dates = []
    for item in orders:
        # TODO: add fullfillment status on real store
        # if orders[item].fulfillment_status == 'fulfilled':
            dates.append(item['created_at'])
    dates.sort()
    return dates[0]

    
# check later with date-time
# def convert_ISO_to_month(ISOdate):
#     local_timezone = pytz.timezone('US/Eastern')
#     local_date = ISOdate.replace(tzinfo=pytz.utc)
#     local_date = local_date.astimezone(local_timezone)
#     return local_date


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
    
    if float(item['total_price']) > 0:
      customerId = item['customer']['id']
      orderDates = datetime.fromisoformat((item['created_at']))
      if not customerId in dict:
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
    customerId = item['customer']['id']
    if not customerId in dict:
      dict[customerId] = [
        { "id": item['id'], "created_at": item['created_at'], "total_price": item["total_price"], }]
    else: 
      dict[customerId].append({
        "id": item['id'],
        "created_at": item['created_at'],
        "total_price": item["total_price"]
      })
      dict[customerId].sort(key=lambda x: x['created_at'])
  
  return dict

def get_previous_order_params_by_order_id (ordersObj, orderId):
  for item in ordersObj:
    if len(ordersObj[item]) > 1:
      for i in range(len(ordersObj[item])-1, -1, -1):
        if ordersObj[item][i]['id'] == orderId:
          prev = ordersObj[item][i - 1]
          return {"date": prev['created_at'], "value": prev['total_price']  }

def get_next_order_params_by_order_id (ordersObj, orderId):
  for item in ordersObj:
    if len(ordersObj[item]) > 1:
      for i in range(0, len(ordersObj[item])-1):
        if ordersObj[item][i]['id'] == orderId:
          next = ordersObj[item][i + 1]
          prev = ordersObj[item][i - 1]
          if next is not None:
            return {"next_date": next["created_at"], "next_value": next["total_price"]}
          if next is None:
            return {"next_date": prev["created_at"], "next_value": prev["total_price"]}

def get_sales_count_by_order_id (ordersObj, orderId):
  for item in ordersObj: 
    for i in range(0, len(ordersObj[item])):
      if ordersObj[item][i]["id"] == orderId: 
        return float(len(ordersObj[item]))
      
    
  
