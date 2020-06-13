import React, { useState, useLayoutEffect, useRef, useEffect } from "react";
import useSyntaxHighlighter from "../../hooks/useSyntaxHighlighter";
import "./Portfolio.scss";

export interface IPortfolio {
  snippets: React.FC[];
}

const Portfolio: React.FC<IPortfolio> = ({ snippets }) => {
  const [dualColumns, setDualColumns] = useState(true);
  const highlightRoot = useSyntaxHighlighter();

  useLayoutEffect(() => {
    if (window) {
      const updateSize = () => setDualColumns(window.innerWidth >= 768);
      window.addEventListener("resize", updateSize);
      updateSize();
      return () => window.removeEventListener("resize", updateSize);
    }
  }, []);

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

      <div className="col-12" ref={highlightRoot}>
        {dualColumns ? (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gridGap: 30 }}>
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
        ) : (
          snippets.map((Snippet, i) => (
            <div key={i} className="snippet">
              <Snippet />
              {i !== snippets.length - 1 && <hr className="my-4" />}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Portfolio;
