let xlsx = require("json-as-xlsx");
export const convertFromJsonToXls = (data: JSON) => {
  let tableinfo = [
    {
      sheet: "Overview",
      columns: [
        { label: "Metrics name", value: "name" },
        { label: "Metrics value", value: "value" },
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
