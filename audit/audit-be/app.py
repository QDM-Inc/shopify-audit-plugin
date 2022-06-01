from datetime import datetime
from flask import Flask, jsonify
from report_service import get_AOV, process_customers_data, get_total_sales, \
    convert_utc_to_local_time, get_first_order_date
from utils import get_response_by_parameter

baseURL = "data-oauth-store.myshopify.com"
apiVersion = "admin/api/2021-10"

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


@app.route('/report')
def get_report():
    customers_data = get_response_by_parameter("customers.json")
    customers = customers_data.customers
    customers_with_types_and_aov = get_AOV(process_customers_data(customers))

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
    report = [{
        'name': "Your total customers",
        'value': customers.length
    }, {
        'name': "What you've made in sales",
        'value': get_total_sales(orders)
    }, {
        'name': "Your shop name",
        'value': shop_data.shop.name
    }, {
        'name': "Your shop was created on",
        'value': convert_utc_to_local_time(shop_data.shop.created_at)
    }, {
        'name': "You started with this amount of products:",
        'value': products_data_first_week.products.length
    }, {
        'name': "You've made your first sale on",
        'value': convert_utc_to_local_time(get_first_order_date(orders))
    }, {
        'name': "In your first month you made:",
        'value': get_total_sales(orders_data_first_month)
    }, {
        'name': "Last month you made",
        'value': get_total_sales(orders_data_last_month)
    }, {
        'name': "First purchase",
        'value': ""
    }, {
        'name': "100th purchase",
        'value': ""
    }, {
        'name': "Largest purchase",
        'value': ""
    }, {
        'name': "You hit ~$10k in sales on",
        'value': ""
    }, {
        'name': "1000th purchase",
        'value': ""
    }, {
        'name': "You hit ~$25k in sales on",
        'value': ""
    }, {
        'name': "You've made total sales for year:",
        'value': ""
    }, {
        'name': "These are your top selling products of all time:",
        'value': "name, total sales, quantity, average quantity per month"
    }, {
        'name': "Top product for top state",
        'value': ""
    }, {
        'name': "Top city for top state",
        'value': ""
    }, {
        'name': "What state is most likely to purchase in the middle of the night?",
        'value': ""
    }, {
        'name': "What city spends the most per person?",
        'value': "city, avg per order, avg per all customers"
    }, {
        'name': "People in this state are most likely to become Repeat customers:",
        'value': ""
    }]
    report1 = [{
        customers: customers_with_types_and_aov
    }, {
        orders: customers_with_types_and_aov
    }]
    return jsonify(report1)
