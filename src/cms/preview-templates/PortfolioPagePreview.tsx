import React from "react";
import { PortfolioPageTemplate } from "../../templates/portfolio-page";

const PortfolioPagePreview = ({ widgetFor }) => {
  return <PortfolioPageTemplate snippets={() => widgetFor("body")} />;
};

export default PortfolioPagePreview;
