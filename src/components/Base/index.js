import React from "react";
import Navigation from "./Navigation";

const Base = ({ children }) => {
  return (
    <>
      <Navigation />

      <main role="main" class="container">
        {children}
      </main>
    </>
  );
};

export default Base;
