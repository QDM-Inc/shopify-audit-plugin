let xlsx = require("json-as-xlsx");
export const convertFromJsonToXls = (data: JSON) => {
  let tableinfo = [
    {
      sheet: "Customers",
      columns: [
        { label: "User", value: "first_name" },
        { label: "Email", value: "email" },
        { label: "Orders quantity", value: "orders_count" },
        { label: "Total spent", value: "total_spent" },
      ],
      content: data,
    },
  ];
  let settings = {
    fileName: "Report",
    extraLength: 3,
    writeOptions: {}, // Style options from https://github.com/SheetJS/sheetjs#writing-options
  };
  xlsx(tableinfo, settings);
};
