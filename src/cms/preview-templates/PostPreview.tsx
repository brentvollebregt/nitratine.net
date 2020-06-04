import React, { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import Prism from "prismjs";
// Would be nice to use: import loadLanguages from "prismjs/components/index"; loadLanguages();
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";
import "prismjs/components/prism-markup";
import "prismjs/components/prism-css";
import { BlogPostTemplate } from "../../templates/blog-post";
import "../../components/Blog/prism-theme.css";

const PostPreview = ({ entry }) => {
  const data = entry.get("data").toJS();

  const root = useRef(null);

  useEffect(() => {
    if (root.current !== null) {
      Prism.highlightAllUnder(root.current);
    }
  }, [data]);

  return (
    <div ref={root}>
      <BlogPostTemplate
        title={data.title || ""}
        date={data.date}
        category={data.category || ""}
        tags={data.tags || []}
        description={data.description || ""}
        hidden={data.hidden || false}
        githubRepository={data.githubRepository || null}
        body={() => <ReactMarkdown source={data.body || ""} />}
        tableOfContents={() => <div className="text-center">Table Of Contents Placeholder</div>}
      />
    </div>
  );
};

export default PostPreview;
