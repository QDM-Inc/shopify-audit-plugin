let xlsx = require("json-as-xlsx");

export const convertFromJsonToXls = (data: any) => {
  let tableinfo = [
    {
      sheet: "Overview",
      columns: [
        { label: "Metrics name", value: "name" },
        { label: "Metrics value", value: "value" },
      ],
      content: data[0].overview,
    },
    {
      sheet: "Sales - Unique Customers",
      columns: [
        { label: "Customer ID", value: "id", format: "#" },
        { label: "Count of Orders", value: "orders_count" },
        { label: "Count of Returns", value: "returns_count" },
        { label: "Count Kept", value: "kept_total" },
        {
          label: "First Purchase Date",
          value: "first_purchase",
          format: "d-mmm-yy",
        },
        {
          label: "Most Recent Purchase Date",
          value: "recent_purchase",
          format: "d-mmm-yy",
        },
        { label: "Total sales", value: "total_spent", format: "$0.00" },
        { label: "AOV", value: "aov", format: "$0.00" },
      ],
      content: data[1].customers,
    },
    {
      sheet: "Sales - Unique Orders",
      columns: [
        { label: "Order name", value: "name" },
        { label: "Month", value: "created_at", format: "mmm-yy" },
        { label: "Order ID", value: "id", format: "#" },
        { label: "Sale kind", value: "sale_kind" },
        { label: "Customer ID", value: "customer.id", format: "#" },
        { label: "Customer Email", value: "email" },
        { label: "Customer type", value: "customer.type" },
        { label: "# of Items", value: "items_count", format: "#" },
        { label: "Ordered Amount", value: "total_price", format: "$0.00" },

        { label: "# of Old Sales", value: "old_sales_count", format: "#" },
        {
          label: "Total Orders",
          value: "customer.orders_count",
          format: "#",
        },
        {
          label: "Most Recent Order Date",
          value: "most_recent_order_date",
          format: "mmm-yy",
        },
        {
          label: "Most Recent Order Value",
          value: "most_recent_order_value",
          format: "$0.00",
        },
        {
          label: "Time since Previous Sale",
          value: "time_since_prev_sale",
          format: "#",
        },
        {
          label: "Price Difference",
          value: "price_diff",
          format: "$0.00",
        },
        {
          label: "Next Purchase Date",
          value: "next_order_date",
          format: "d-mmm-yy",
        },
        {
          label: "Next Purchase Amount",
          value: "next_order_value",
          format: "$0.00",
        },
        {
          label: "Months after",
          value: "months_after",
          format: "#",
        },
        {
          label: "Next Purchase Price Difference",
          value: "next_price_diff",
          format: "$0.00",
        },
      ],
      content: data[2].orders,
    },
  ];
  let settings = {
    fileName: `Report for ${data[3].name}`,
    extraLength: 3,
    writeOptions: {}, // Style options from https://github.com/SheetJS/sheetjs#writing-options
  };
  xlsx(tableinfo, settings);
};
