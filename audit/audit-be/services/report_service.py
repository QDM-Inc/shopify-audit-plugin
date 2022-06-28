from datetime import datetime

import pytz


def get_total_sales(orders):
    sales = []
    if len(orders) >= 1:
        for item in orders:
            sales.append(item['total_price'])
        total = sum(sales)

        return round(total, 2)
    else:
        return 'No orders found'


def convert_utc_to_local_time(utc_date):
    local_timezone = pytz.timezone('US/Eastern')
    utc_date = str(utc_date)
    date_time_obj = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S%z")
    local_date = date_time_obj.replace(tzinfo=pytz.utc)
    local_date = local_date.astimezone(local_timezone)
    return local_date


def get_first_order_date(orders):
    dates = []
    for item in orders:
        # TODO: add fullfillment status on real store
        # if orders[item].fulfillment_status == 'fulfilled':
        dates.append(datetime.fromisoformat(item['created_at']))
    dates.sort()
    return dates[0]

def get_month_of_order(date):
    return f'{datetime.strptime(str(datetime.fromisoformat(date).month), "%m").strftime("%b")} {datetime.fromisoformat(date).year}'


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
    dictionary = {}
    for item in orders:
        if float(item['total_price']) > 0:
            customer_id = item['customer']['id']
            order_dates = datetime.fromisoformat((item['created_at']))
            if customer_id not in dictionary:
                dictionary[customer_id] = [order_dates]
            else:
                dictionary[customer_id].append(order_dates)
                dictionary[customer_id].sort()
        else:
            return 'order price<0'
    return dictionary


def group_orders_by_customer_id(orders):
    dictionary = {}
    for item in orders:
        customer_id = item['customer']['id']
        if customer_id not in dictionary:
            dictionary[customer_id] = [
                {"id": item['id'], "created_at": item['created_at'], "total_price": item["total_price"], }]
        else:
            dictionary[customer_id].append({
                "id": item['id'],
                "created_at": item['created_at'],
                "total_price": item["total_price"]
            })
            dictionary[customer_id].sort(key=lambda x: x['created_at'])

    return dictionary


def get_previous_order_params_by_order_id(orders_obj, order_id):
    for item in orders_obj:
        if len(orders_obj[item]) > 1:
            for i in range(len(orders_obj[item]) - 1, -1, -1):
                if orders_obj[item][i]['id'] == order_id:
                    prev_el = orders_obj[item][i - 1]
                    return {"date": prev_el['created_at'], "value": prev_el['total_price']}


def get_next_order_params_by_order_id(orders_obj, order_id):
    for item in orders_obj:
        if len(orders_obj[item]) > 1:
            for i in range(0, len(orders_obj[item]) - 1):
                if orders_obj[item][i]['id'] == order_id:
                    next_el = orders_obj[item][i + 1]
                    prev_el = orders_obj[item][i - 1]
                    if next_el is not None:
                        return {"next_date": next_el["created_at"], "next_value": next_el["total_price"]}
                    if next_el is None:
                        return {"next_date": prev_el["created_at"], "next_value": prev_el["total_price"]}


def get_sales_count_by_order_id(orders_obj, order_id):
    for item in orders_obj:
        for i in range(0, len(orders_obj[item])):
            if orders_obj[item][i]["id"] == order_id:
                return float(len(orders_obj[item]))

def get_marketing_consent(item):
    if item["marketing_opt_in_level"]=="confirmed_opt_in" and item["sms_marketing_consent"]["state"]=="subscribed":
        return "sms, email"
    if item["sms_marketing_consent"]["state"]=="subscribed" and item["marketing_opt_in_level"]== None:
        return "sms"
    if item["marketing_opt_in_level"]=="confirmed_opt_in" and item["sms_marketing_consent"]["state"]!="subscribed":
        return "email"
    
    else: return "none"


def count_contact_info(item):
    counter=0
    if item["email"] and item["phone"]:
        return counter+2
    if item["email"]:
       return counter+1
    if item["phone"]:
       return counter+1
    
    else: return counter
    
    

