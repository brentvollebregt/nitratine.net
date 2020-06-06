import React from "react";
import "./Portfolio.scss";

export interface IPortfolio {
  leftContent: React.FC;
  rightContent: React.FC;
}

const Portfolio: React.FC<IPortfolio> = ({ leftContent, rightContent }) => {
  const LeftContent = leftContent;
  const RightContent = rightContent;

  return (
    <div className="row justify-content-center mb-5">
      <div className="col-xs-12 col-lg-8">
        <h1 className="text-center">Portfolio</h1>
        <p className="lead text-center">
          This is a small collection of my favourite projects I developed with a small description
          and links to pages relating to the project.
        </p>
      </div>

      <div className="col-sm-12 col-md-6 col-centered">
        <LeftContent />
      </div>
      <div className="col-xs-12 col-sm-6 col-centered">
        <RightContent />
      </div>
    </div>
  );
};

export default Portfolio;
