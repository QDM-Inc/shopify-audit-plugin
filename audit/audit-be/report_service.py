from datetime import datetime

import pytz

def get_total_sales(orders):
    sales = []
    if orders.length >= 1:
        for item in orders:
            sales.append(float(orders[item].total_price))

        total = sum(sales)
        return round(total, 2)
    else:
        return "No orders found"


def get_first_order_date(orders):
    dates = []

    for item in orders:
        # TODO: add fullfillment status on real store
        if orders[item].fulfillment_status == 'fulfilled':
            dates.append(datetime.fromisoformat((orders[item].created_at)))

    dates.sort()
    return dates[0]


def convert_utc_to_local_time(utc_date):
    local_timezone = pytz.timezone("US/Eastern")
    local_date = utc_date.replace(tzinfo=pytz.utc)
    local_date = local_date.astimezone(local_timezone)
    return local_date


def process_customers_data(data):
    for customer in data:
        if data[customer].orders_count > 1:
            data[customer]["type"] = "Returning"
        else:
            data[customer]["type"] = "First-time"

    return data


def get_AOV(data):
    for customer in data:
        data[customer]["aov"] = data[customer].total_spent / data[customer].orders_count
    return data