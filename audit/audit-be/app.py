from datetime import date, datetime
import datetime as datetime2
import json
from flask import Flask, jsonify

from shopify.routes import shopify_bp
from utils.utils import get_response_by_parameter
from services.report_service import process_customers_data, \
    convert_utc_to_local_time, get_first_order_date, get_order_dates_by_customer_id, \
    get_previous_order_params_by_order_id, group_orders_by_customer_id, get_next_order_params_by_order_id, get_total_sales, get_month_of_order

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.register_blueprint(shopify_bp)


@app.route("/report")
def get_report():
    customers_data = get_response_by_parameter("customers.json")
    customers_list = customers_data["customers"]
    customers_with_types_and_aov = process_customers_data(customers_list)
    shop_data = get_response_by_parameter("shop.json?fields=name,created_at")
    store_creation_date = (shop_data["shop"]["created_at"])
    week_delta = datetime2.timedelta(days=7)
    store_creation_date_str = datetime.strptime(store_creation_date,"%Y-%m-%dT%H:%M:%S%z")
    first_week_date = (store_creation_date_str + week_delta)
    now_date = datetime.now()
    orders_data = get_response_by_parameter("orders.json?status=any")
    orders = orders_data["orders"]
    products_data_first_week = get_response_by_parameter("products.json?created_at_max=" + f'{first_week_date}')
    order_dates_by_customer_id = get_order_dates_by_customer_id(orders)
    orders_by_customer_id = group_orders_by_customer_id(orders)

    # marketing_data = get_response_by_parameter("marketing_events.json")

    def new_orders():
        for item in orders:
            item["created_at_month"] = get_month_of_order(item["created_at"])
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
                item["most_recent_order_date"] = datetime.fromisoformat(prev_orders_by_id["date"])
                item["most_recent_order_date_value"] = datetime.date(item["most_recent_order_date"])
                item["most_recent_order_value"] = float(prev_orders_by_id["value"])
                item["time_since_prev_sale"] =  datetime.fromisoformat(item["created_at"]) - (item["most_recent_order_date"])
                item["price_diff"] = item["total_price"] - item["most_recent_order_value"]

            if next_orders_by_id is not None:
                item["next_order_date"] = datetime.fromisoformat(next_orders_by_id["next_date"])
                item["next_order_date_value"] = datetime.date(item["next_order_date"])
                item["next_order_value"] = float(next_orders_by_id["next_value"])
                item["months_after"] = datetime.fromisoformat(item["created_at"]) - (item["next_order_date"])
                item["next_price_diff"] = item["total_price"] - item["next_order_value"]
        

        return orders

    def new_customers():
        for index in customers_with_types_and_aov:
            index["total_spent"] = float(index["total_spent"])
            item = str(index["id"])

            for customer_id in order_dates_by_customer_id:
                if str(customer_id) == item:
                    index["recent_purchase"] = datetime.date(order_dates_by_customer_id[customer_id][0])
                    index["first_purchase"] = datetime.date(order_dates_by_customer_id[customer_id][-1])

        return customers_with_types_and_aov

    report = [{"name": "Your total customers", "value": float(len(customers_list))},
              {
                  "name": "What you've made in sales ($)",
                  "value": get_total_sales(new_orders()),
              },
              {"name": "Your shop name", "value": shop_data["shop"]["name"]},
              {
                  "name": "Your shop was created on",
                  "value": datetime.date(convert_utc_to_local_time(shop_data["shop"]["created_at"])),
              },
              {
                  "name": "You started with this amount of products:",
                  "value": len(products_data_first_week["products"]),
              },
              
               {
                  "name": "You've made your first sale on",
                  "value": datetime.date(get_first_order_date(orders))
              },
         
              ]

    report1 = {"data": [
        {"overview": report},
        {"customers": new_customers()},
        {"orders": new_orders()},
        {"name": f'{shop_data["shop"]["name"]} {datetime.date(now_date)}'}
    ]}

    class DatetimeEncoder(json.JSONEncoder):
        def default(self, obj):
            try:
                return super().default(obj)
            except TypeError:
                return str(obj)

    return json.dumps(report1, cls=DatetimeEncoder)

