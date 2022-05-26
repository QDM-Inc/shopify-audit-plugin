import React, { useState } from "react";
import Button from "../button/button";
import styles from "./App.module.css";
import { LoadingState } from "../button/button";
import { convertFromJsonToXls } from "../../utils/jsontoexcel";

const apiURL = "customers";

function App() {
  const [reportState, setReportState] = useState<LoadingState>("");
  const getReport = async () => {
    setReportState("pending");

    // timeout set to check loading state
    setTimeout(async () => {
      const response = await fetch(apiURL);

      if (response.status === 200) {
        const data = response.json();
        data.then((res) => {
          setReportState("success");
          convertFromJsonToXls(res.customers);
        });
      } else {
        setReportState("failure");
      }
    }, 3000);
  };

  const handleClick = () => {
    getReport();
  };

  const defaultTitle = "To get all of your store audit";
  const pendingTitle = "Figuring out the report...";
  const successTitle = "Report downloaded";
  const failureTitle =
    "Report download failed 😔 Please reload the page and try again";

  const getTitle = (state?: string) => {
    switch (state) {
      case "pending":
        return pendingTitle;
      case "failure":
        return failureTitle;
      case "success":
        return successTitle;
      default:
        return defaultTitle;
    }
  };
  return (
    <div className={styles.app}>
      <div className={styles.title}>{getTitle(reportState)}</div>
      <Button state={reportState} onClick={handleClick} />
    </div>
  );
}

export default App;
