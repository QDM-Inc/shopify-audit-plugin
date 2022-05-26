import React from "react";
import styles from "./button.module.css";
import { ReactComponent as LoadingIcon } from "./icons/loading.svg";
import { ReactComponent as FailIcon } from "./icons/fail.svg";
import { ReactComponent as SuccessIcon } from "./icons/success.svg";
import classNames from "classnames";
export type LoadingState = "pending" | "success" | "failure" | "";

export interface ButtonProps {
  state: LoadingState;
  onClick: () => void;
}

const Button = (props: ButtonProps) => {
  const { state, onClick } = props;
  const buttonText = "Click here";
  const buttonCN = classNames(styles.container, {
    [styles.containerOnLoad]: state === "pending",
    [styles.containerOnLoaded]: state === "success" || state === "failure",
  });

  return (
    <button className={buttonCN} onClick={onClick} disabled={state !== ""}>
      <>
        {state === "" && buttonText}
        {state === "pending" && (
          <div className={styles.loadingIconWrapper}>
            <LoadingIcon className={styles.loadingIcon} />
          </div>
        )}
        {state === "failure" && (
          <div className={styles.loadingIconWrapper}>
            <FailIcon />
          </div>
        )}
        {state === "success" && (
          <div className={styles.loadingIconWrapper}>
            <SuccessIcon />
          </div>
        )}
      </>
    </button>
  );
};

export default Button;
