import React from "react";
import ReactMarkdown from "react-markdown";
import { PortfolioPageTemplate } from "../../templates/portfolio-page";

const PortfolioPagePreview = ({ entry }) => {
  const data = entry.get("data").toJS();
  return (
    <PortfolioPageTemplate
      snippets={data.snippets.map(s => () => <ReactMarkdown source={s.body} />)}
    />
  );
};

export default PortfolioPagePreview;
