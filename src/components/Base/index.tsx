import React from "react";
import Navigation from "./Navigation";
import "./all.scss";

const Base = ({ children }) => {
  return (
    <>
      <Navigation />

      <main role="main" className="container">
        {children}
      </main>
    </>
  );
};

export default Base;
