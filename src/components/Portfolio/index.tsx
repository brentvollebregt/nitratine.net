import React from "react";
import "./Portfolio.scss";

export interface IPortfolio {
  snippets: React.FC[];
}

const Portfolio: React.FC<IPortfolio> = ({ snippets }) => {
  const leftSnippets = snippets.filter((_, i) => i % 2 === 0);
  const rightSnippets = snippets.filter((_, i) => i % 2 === 1);

  return (
    <div className="portfolio row justify-content-center">
      <div className="col-xs-12 col-lg-8">
        <h1 className="text-center">Portfolio</h1>
        <p className="lead text-center">
          This is a small collection of my favourite projects I developed with a small description
          and links to pages relating to the project.
        </p>
      </div>

      {/* Dual column */}
      <div className="dual-column col-12">
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gridGap: 10 }}>
          <div>
            {leftSnippets.map((Snippet, i) => (
              <div key={i} className="snippet">
                <Snippet />
                {i !== leftSnippets.length - 1 && <hr className="my-4" />}
              </div>
            ))}
          </div>
          <div>
            {rightSnippets.map((Snippet, i) => (
              <div key={i} className="snippet">
                <Snippet />
                {i !== rightSnippets.length - 1 && <hr className="my-4" />}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Single column */}
      <div className="single-column col-12">
        {snippets.map((Snippet, i) => (
          <div key={i} className="snippet">
            <Snippet />
            {i !== snippets.length - 1 && <hr className="my-4" />}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Portfolio;
