import React, { useEffect } from "react";
import useSyntaxHighlighter from "../../hooks/useSyntaxHighlighter";
import "./Portfolio.scss";
import SEO from "../Helpers/SEO";

export interface IPortfolio {
  snippets: React.FC;
}

const Portfolio: React.FC<IPortfolio> = ({ snippets }) => {
  const highlightRoot = useSyntaxHighlighter();

  // Due the required usage of CSS order, the size of the div wrapping the snippets is the same height as if no order were applied.
  // To get around that situation, this calculates how high the columns should be based off the snippets height per-column.
  // The tallest column's height is then what the wrapper is set to (+50, I don't know why but it works.)
  useEffect(() => {
    if (window) {
      const updateSize = () => {
        if (highlightRoot.current !== null) {
          const snippetNodes = highlightRoot.current.querySelectorAll(".snippet");
          const columnHeights = Array.from(snippetNodes).reduce((acc, curr) => {
            const order = (curr as any).computedStyleMap()?.get("order") ?? 1;
            const height = curr.getBoundingClientRect().height;
            return {
              ...acc,
              [order.value]: (acc[order.value] ?? 0) + height
            };
          }, {} as { [key: string]: number });

          const snippetContainer = highlightRoot.current.querySelector("div")!;
          snippetContainer.style.height = `${Math.max(...Object.values(columnHeights), 0) + 50}px`;
        }
      };
      window.addEventListener("resize", updateSize);
      updateSize();
      return () => window.removeEventListener("resize", updateSize);
    }
  }, []);

  const Snippets = snippets;

  return (
    <>
      <SEO
        title="Portfolio"
        description="This is a small collection of my favourite projects I developed with a small description and links to pages relating to the project."
        relativePath="/portfolio/"
      />
      <div className="portfolio">
        <div className="col-xs-12 col-lg-8 d-block mx-auto">
          <h1 className="text-center">Portfolio</h1>
          <p className="lead text-center">
            This is a small collection of my favourite projects I developed with a small description
            and links to pages relating to the project.
          </p>
        </div>

        <div className="d-flex mw-100 masonry" ref={highlightRoot}>
          <Snippets />
        </div>
      </div>
    </>
  );
};

export default Portfolio;
