const https = require("https");
const fetch = require("node-fetch");
const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());

let port = process.env.PORT;
if (port == null || port == "") {
  port = 5000;
}
app.listen(port, function () {
  console.log(`Server started successfully on ${port}`);
});

app.get("/customers", async (req, res) => {
  const baseURL = "data-oauth-store.myshopify.com";
  const apiVersion = "admin/api/2021-10";
  const customers_response = await fetch(
    `https://${baseURL}/${apiVersion}/customers.json`,
    {
      headers: {
        Host: `${baseURL}`,
        "X-Shopify-Access-Token": "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",
        "Content-Type": "application/json",
      },
    }
  );

  const customers_data = await customers_response.json();

  res.json(customers_data);
});
