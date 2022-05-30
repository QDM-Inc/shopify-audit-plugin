const https = require("https");
const fetch = require("node-fetch");
const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());

const baseURL = "data-oauth-store.myshopify.com";
const apiVersion = "admin/api/2021-10";

let port = process.env.PORT;
if (port == null || port == "") {
  port = 5000;
}
app.listen(port, function () {
  console.log(`Server started successfully on ${port}`);
});

const getResponseByParameter = async (parameter) => {
  const response = await fetch(
    `https://${baseURL}/${apiVersion}/${parameter}`,
    {
      headers: {
        Host: `${baseURL}`,
        "X-Shopify-Access-Token": "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",
        "Content-Type": "application/json",
      },
    }
  );
  return response.json();
};

const getTotalSales = (orders) => {
  //TODO: should we count in refunds?
  let sales = [];
  if (orders.length >= 1) {
    for (let item in orders) {
      sales.push(Number(orders[item].total_price));
    }
    const total = sales.reduce((acc, val) => {
      return acc + val;
    }, 0);
    console.timeLog();
    return total.toFixed(2);
  } else {
    return "No orders found";
  }
};

const getFirstOrderDate = (orders) => {
  let dates = [];
  for (let item in orders) {
    //TODO:  add fullfillment status on real store
    // if(orders[item].fulfillment_status==='fulfilled'){
    dates.push(new Date(orders[item].created_at));
    // }
  }

  const sorted = dates.sort((a, b) => {
    return a - b;
  });

  return sorted.shift();
};

const convertUTCToLocalTime = (date) => {
  let localDate = new Date(date);
  let options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  return localDate.toLocaleString("en-US", options);
};

app.get("/customers", async (req, res) => {
  //customers
  const customers_data = await getResponseByParameter("customers.json");
  const customers = customers_data.customers;

  //shop
  const shop_data = await getResponseByParameter(
    "shop.json?fields=name,created_at"
  );

  //dates
  const storeCreationDate = new Date(shop_data.shop.created_at);
  const firstMonthEndDate = new Date(
    storeCreationDate.getFullYear(),
    storeCreationDate.getMonth() + 1,
    storeCreationDate.getDate() + 1
  );
  const firstWeekDate = new Date(
    storeCreationDate.getFullYear(),
    storeCreationDate.getMonth(),
    storeCreationDate.getDate() + 7
  );
  const nowDate = new Date();
  const lastMonthBeginDate = new Date(
    nowDate.getFullYear(),
    nowDate.getMonth()
  );

  //orders
  const orders_data = await getResponseByParameter("orders.json?status=any");
  const orders = orders_data.orders;
  const orders_data_first_month = await getResponseByParameter(
    `orders.json?created_at_max=${firstMonthEndDate}`
  );
  const orders_data_last_month = await getResponseByParameter(
    `orders.json?created_at_min=${lastMonthBeginDate}`
  );

  //products
  const products_data = await getResponseByParameter("products.json");
  const products = products_data.products;
  const products_data_first_week = await getResponseByParameter(
    `products.json?created_at_max=${firstWeekDate}`
  );

  const report = [
    { name: "Your total customers", value: customers.length },
    { name: "What you've made in sales", value: getTotalSales(orders) },
    { name: "Your shop name", value: shop_data.shop.name },
    {
      name: "Your shop was created on",
      value: convertUTCToLocalTime(shop_data.shop.created_at),
    },
    {
      name: "You started with this amount of products:",
      value: products_data_first_week.products.length,
    },
    {
      name: "You've made your first sale on",
      value: convertUTCToLocalTime(getFirstOrderDate(orders)),
    },
    {
      name: "In your first month you made:",
      value: getTotalSales(orders_data_first_month),
    },
    {
      name: "Last month you made",
      value: getTotalSales(orders_data_last_month),
    },
    { name: "First purchase", value: "" },
    { name: "100th purchase", value: "" },
    { name: "Largest purchase", value: "" },
    { name: "You hit ~$10k in sales on", value: "" },
    { name: "1000th purchase", value: "" },
    { name: "You hit ~$25k in sales on", value: "" },
    { name: "You've made total sales for year:", value: "" },
    {
      name: "These are your top selling products of all time:",
      value: "name, total sales, quantity, average quantity per month",
    },
    { name: "Top product for top state", value: "" },
    { name: "Top city for top state", value: "" },
    {
      name: "What state is most likely to purchase in the middle of the night?",
      value: "",
    },
    {
      name: "What city spends the most per person?",
      value: "city, avg per order, avg per all customers",
    },
    {
      name: "People in this state are most likely to become Repeat customers:",
      value: "",
    },
  ];

  res.json(report);
});
