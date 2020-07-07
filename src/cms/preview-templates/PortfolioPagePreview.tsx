import React from "react";
import { LocationProvider } from "@reach/router";
import { PortfolioPageTemplate } from "../../templates/portfolio-page";

const PortfolioPagePreview = ({ widgetFor }) => {
  return (
    <LocationProvider>
      <div className="mx-1">
        <PortfolioPageTemplate snippets={() => widgetFor("body")} />
      </div>
    </LocationProvider>
  );
};

export default PortfolioPagePreview;
