import { createElement, memo, useState } from "react";
import { convertFromJsonToXls } from "../../utils/jsontoexcel";
import { LoadingState } from "../button/button";
import App from "./app.component";
const apiURL = "report";

export const AppContainer = memo(() => {
  const [reportState, setReportState] = useState<LoadingState>("");
  const getReport = async () => {
    setReportState("pending");

    const response = await fetch(apiURL);

    if (response.status === 200) {
      const data = response.json();
      data.then((res) => {
        setReportState("success");
        convertFromJsonToXls(res);
      });
    } else {
      setReportState("failure");
    }
  };

  const handleClick = () => {
    getReport();
  };

  return createElement(App, { reportState, handleClick });
});
