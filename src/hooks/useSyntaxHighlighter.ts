import { useRef, useEffect } from "react";
import Prism from "prismjs";
// Would be nice to use: import loadLanguages from "prismjs/components/index"; loadLanguages();
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";
import "prismjs/components/prism-markup";
import "prismjs/components/prism-css";
import "../components/Blog/prism-theme.scss";

const useSyntaxHighlighter = () => {
  const root = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (root.current !== null) {
      Prism.highlightAllUnder(root.current);
      console.log("highlightAllUnder");
    }
  });

  return root;
};

export default useSyntaxHighlighter;
