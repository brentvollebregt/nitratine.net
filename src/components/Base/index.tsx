import React from "react";
import Navigation from "./Navigation";
import "./all.scss";

const Base = ({ children }) => {
  return (
    <>
      <Navigation />
      <main role="main" className="container mt-4">
        {children}
      </main>
    </>
  );
};

export default Base;
