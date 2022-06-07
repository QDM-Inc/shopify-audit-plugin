from datetime import datetime
from time import time
from flask import Flask, jsonify
from utils import get_response_by_parameter
from report_service import process_customers_data, get_total_sales, \
    convert_utc_to_local_time, get_first_order_date, get_order_dates_by_customer_id, convert_ISO_to_month




app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=5000)
    while True: 
        time.sleep(30)


@app.route('/report')
def get_report():
    customers_data = get_response_by_parameter("customers.json")
    customers = customers_data.customers
    customers_with_types_and_aov = process_customers_data(customers)

    shop_data = get_response_by_parameter("shop.json?fields=name,created_at")

    store_creation_date = datetime.fromisoformat(shop_data.shop.created_at)
    first_month_end_date = datetime(store_creation_date.year, store_creation_date.month + 1,
                                    store_creation_date.day + 1)
    first_week_date = datetime(store_creation_date.year, store_creation_date.month, store_creation_date.day + 7)
    now_date = datetime.now()
    last_month_begin_date = datetime(now_date.year, now_date.month, 1)
   
    orders_data = get_response_by_parameter("orders.json?status=any")
    orders = orders_data.orders
    orders_data_first_month = get_response_by_parameter("orders.json?created_at_max=".concat(first_month_end_date))
    orders_data_last_month = get_response_by_parameter("orders.json?created_at_min=".concat(last_month_begin_date))

    products_data = get_response_by_parameter("products.json")
    products = products_data.products
    products_data_first_week = get_response_by_parameter("products.json?created_at_max=".concat(first_week_date))

    marketing_data = get_response_by_parameter("marketing_events.json")

    order_dates_by_customer_id = get_order_dates_by_customer_id(orders)


    def new_orders():
        for item in orders:
            for index in customers_with_types_and_aov:
                if orders[item].customer.id == customers_with_types_and_aov[index].id:
                    orders[item].customer["type"] = customers_with_types_and_aov[index].type
                
                customers_with_types_and_aov[index]["returns_count"] = float(len(orders[item].refunds))

                customers_with_types_and_aov[index]["kept_total"] = float(customers_with_types_and_aov[index].orders_count) - float(customers_with_types_and_aov[index]["returns_count"])

                if orders[item].total_price > 0:
                    customers_with_types_and_aov[index].aov = customers_with_types_and_aov[index].total_spent / customers_with_types_and_aov[index]["kept_total"]
            
            orders[item].created_at = convert_ISO_to_month(orders[item].created_at)
        
        return orders
  
    def new_customers():
        for index in customers_with_types_and_aov:
            item = customers_with_types_and_aov[index]
            item.total_spent = float(item.total_spent)
            if item.id in order_dates_by_customer_id:
                item.recent_purchase = convert_utc_to_local_time(order_dates_by_customer_id[item.id][0])
                item.first_purchase = convert_utc_to_local_time(order_dates_by_customer_id[item.id][-1])
                        
        return customers_with_types_and_aov
    

    report = [ { 'name': "Your total customers", 'value': float(len(customers)) },
    {
      'name': "What you've made in sales ($)",
      'value': get_total_sales(new_orders()),
    },
    { 'name': "Your shop name", 'value': shop_data.shop.name },
    {
      'name': "Your shop was created on",
      'value': convert_utc_to_local_time(shop_data.shop.created_at),
    },
    {
      'name': "You started with this amount of products:",
      'value': len(products_data_first_week[products]),
    }, {
        'name': "You've made your first sale on",
        'value': convert_utc_to_local_time(get_first_order_date(orders))
    }, {
        'name': "In your first month you made:",
        'value': get_total_sales(orders_data_first_month)
    }, {
        'name': "Last month you made",
        'value': get_total_sales(orders_data_last_month)
    }, 
    # {
    #     'name': "First purchase",
    #     'value': ""
    # }, {
    #     'name': "100th purchase",
    #     'value': ""
    # }, {
    #     'name': "Largest purchase",
    #     'value': ""
    # }, {
    #     'name': "You hit ~$10k in sales on",
    #     'value': ""
    # }, {
    #     'name': "1000th purchase",
    #     'value': ""
    # }, {
    #     'name': "You hit ~$25k in sales on",
    #     'value': ""
    # }, {
    #     'name': "You've made total sales for year:",
    #     'value': ""
    # }, {
    #     'name': "These are your top selling products of all time:",
    #     'value': "name, total sales, quantity, average quantity per month"
    # }, {
    #     'name': "Top product for top state",
    #     'value': ""
    # }, {
    #     'name': "Top city for top state",
    #     'value': ""
    # }, {
    #     'name': "What state is most likely to purchase in the middle of the night?",
    #     'value': ""
    # }, {
    #     'name': "What city spends the most per person?",
    #     'value': "city, avg per order, avg per all customers"
    # }, {
    #     'name': "People in this state are most likely to become Repeat customers:",
    #     'value': ""
    # }
    ]
 
    report1 = [
    { 'overview': report },
    { 'customers': new_customers() },
    { 'orders': new_orders() },
  ]
    return jsonify(report1)
