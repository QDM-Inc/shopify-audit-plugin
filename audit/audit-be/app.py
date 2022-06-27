from datetime import datetime
from flask import Flask, jsonify

from shopify.routes import shopify_bp
from utils.utils import get_response_by_parameter
from services.report_service import process_customers_data, \
    convert_utc_to_local_time, get_first_order_date, get_order_dates_by_customer_id, \
    get_previous_order_params_by_order_id, group_orders_by_customer_id, get_next_order_params_by_order_id, get_total_sales

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.register_blueprint(shopify_bp)


@app.route("/report")
def get_report():
    customers_data = get_response_by_parameter("customers.json")
    customers_list = customers_data["customers"]

    customers_with_types_and_aov = process_customers_data(customers_list)
    shop_data = get_response_by_parameter("shop.json?fields=name,created_at")

    store_creation_date = datetime.fromisoformat(shop_data["shop"]["created_at"])
    first_month_end_date = datetime(store_creation_date.year, store_creation_date.month + 1,
                                    store_creation_date.day + 1)
    first_week_date = datetime(store_creation_date.year, store_creation_date.month, store_creation_date.day + 7)
    now_date = datetime.now()
    last_month_begin_date = datetime(now_date.year, now_date.month, 1)

    orders_data = get_response_by_parameter("orders.json?status=any")
    orders = orders_data["orders"]
    orders_data_first_month = get_response_by_parameter("orders.json?created_at_max=" + f'{first_month_end_date}')
    orders_data_last_month = get_response_by_parameter("orders.json?created_at_min=" + f'{last_month_begin_date}')

    products_data = get_response_by_parameter("products.json")
    products = products_data["products"]
    products_data_first_week = get_response_by_parameter("products.json?created_at_max=" + f'{first_week_date}')

    # marketing_data = get_response_by_parameter("marketing_events.json")

    order_dates_by_customer_id = get_order_dates_by_customer_id(orders)
    orders_by_customer_id = group_orders_by_customer_id(orders)

    def new_orders():
        for item in orders:
            for index in customers_with_types_and_aov:
                if item["customer"]["id"] == index["id"]:
                    item["customer"]["type"] = index["type"]

                index["returns_count"] = float(len(item["refunds"]))

                index["kept_total"] = float(
                    index["orders_count"]) - float(index["returns_count"])

                if float(item["total_price"]) > 0 and float(index["kept_total"]) > 0:
                    index["aov"] = float(index["total_spent"]) / float(index["kept_total"])

            item["items_count"] = float(len(item["line_items"]))
            item["total_price"] = float(item["total_price"])

            if len(item["refunds"]) > 0:
                item["sale_kind"] = "refund"
            else:
                item["sale_kind"] = "order"

            prev_orders_by_id = get_previous_order_params_by_order_id(orders_by_customer_id, item["id"])
            next_orders_by_id = get_next_order_params_by_order_id(orders_by_customer_id, item["id"])

            if prev_orders_by_id is not None:
                item["most_recent_order_date"] = (prev_orders_by_id["date"])
                item["most_recent_order_value"] = float(prev_orders_by_id["value"])
                item["time_since_prev_sale"] =  datetime.fromisoformat(item["created_at"]) - datetime.fromisoformat(item["most_recent_order_date"])
                item["price_diff"] = item["total_price"] - item["most_recent_order_value"]

            if next_orders_by_id is not None:
                item["next_order_date"] = (next_orders_by_id["next_date"])
                item["next_order_value"] = float(next_orders_by_id["next_value"])
                item["months_after"] = datetime.fromisoformat(item["created_at"]) - datetime.fromisoformat(item["next_order_date"])
                item["next_price_diff"] = item["total_price"] - item["next_order_value"]

        return orders

    def new_customers():
        for index in customers_with_types_and_aov:
            index["total_spent"] = float(index["total_spent"])
            item = str(index["id"])

            for customer_id in order_dates_by_customer_id:
                if str(customer_id) == item:
                    index["recent_purchase"] = order_dates_by_customer_id[customer_id][0]
                    index["first_purchase"] = order_dates_by_customer_id[customer_id][-1]

        return customers_with_types_and_aov

    report = [{"name": "Your total customers", "value": float(len(customers_list))},
              {
                  "name": "What you've made in sales ($)",
                  "value": get_total_sales(new_orders()),
              },
              {"name": "Your shop name", "value": shop_data["shop"]["name"]},
              {
                  "name": "Your shop was created on",
                  "value": convert_utc_to_local_time(shop_data["shop"]["created_at"]),
              },
              {
                  "name": "You started with this amount of products:",
                  "value": len(products_data_first_week["products"]),
              }, {
                  "name": "You've made your first sale on",
                  "value": get_first_order_date(orders)
              },
              # {
              #     "name": "In your first month you made:",
              #     "value": get_total_sales(orders_data_first_month)
              # }, {
              #     "name": "Last month you made",
              #     "value": get_total_sales(orders_data_last_month)
              # },
              # {
              #     "name": "First purchase",
              #     "value": ""
              # }, {
              #     "name": "100th purchase",
              #     "value": ""
              # }, {
              #     "name": "Largest purchase",
              #     "value": ""
              # }, {
              #     "name": "You hit ~$10k in sales on",
              #     "value": ""
              # }, {
              #     "name": "1000th purchase",
              #     "value": ""
              # }, {
              #     "name": "You hit ~$25k in sales on",
              #     "value": ""
              # }, {
              #     "name": "You"ve made total sales for year:",
              #     "value": ""
              # }, {
              #     "name": "These are your top selling products of all time:",
              #     "value": "name, total sales, quantity, average quantity per month"
              # }, {
              #     "name": "Top product for top state",
              #     "value": ""
              # }, {
              #     "name": "Top city for top state",
              #     "value": ""
              # }, {
              #     "name": "What state is most likely to purchase in the middle of the night?",
              #     "value": ""
              # }, {
              #     "name": "What city spends the most per person?",
              #     "value": "city, avg per order, avg per all customers"
              # }, {
              #     "name": "People in this state are most likely to become Repeat customers:",
              #     "value": ""
              # }
              ]

    report1 = {"data": [
        {"overview": report},
        {"customers": new_customers()},
        {"orders": new_orders()},
        {"name": f'{shop_data["shop"]["name"]} {now_date}'}
    ]}

    return jsonify(report1)
