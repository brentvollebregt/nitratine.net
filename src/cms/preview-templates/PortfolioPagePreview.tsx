import React from "react";
import { PortfolioPageTemplate } from "../../templates/portfolio-page";

const PortfolioPagePreview = ({ widgetFor }) => {
  return (
    <div className="mx-1">
      <PortfolioPageTemplate snippets={() => widgetFor("body")} />
    </div>
  );
};

export default PortfolioPagePreview;
