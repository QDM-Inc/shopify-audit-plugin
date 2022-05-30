import React from "react";
import Button from "../button/button";
import styles from "./App.module.css";
import { LoadingState } from "../button/button";

export interface AppProps {
  reportState: LoadingState;
  handleClick: () => void;
}

export const App = (props: AppProps) => {
  const { reportState, handleClick } = props;

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
};

export default App;
