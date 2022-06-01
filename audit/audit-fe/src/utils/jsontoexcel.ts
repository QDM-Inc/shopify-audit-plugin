let xlsx = require("json-as-xlsx");
export const convertFromJsonToXls = (data: any) => {
  let tableinfo = [
    // {
    //   sheet: "Overview",
    //   columns: [
    //     { label: "Metrics name", value: "name" },
    //     { label: "Metrics value", value: "value" },
    //   ],
    //   content: data,
    // },
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
      content: data[0].customers,
    },
    {
      sheet: "Sales - Unique Orders",
      columns: [
        { label: "Customer ID", value: "id", format: "#" },
        { label: "Customer Email", value: "email" },
        { label: "Customer type", value: "type" },
      ],
      content: data[1].orders,
    },
  ];
  let settings = {
    fileName: "Report",
    extraLength: 3,
    writeOptions: {}, // Style options from https://github.com/SheetJS/sheetjs#writing-options
  };
  xlsx(tableinfo, settings);
};
