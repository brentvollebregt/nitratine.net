import React from "react";
import useSyntaxHighlighter from "../../hooks/useSyntaxHighlighter";
import { BlogPostTemplate } from "../../templates/blog-post";
import { IPagination } from "../../components/Blog/Post/Pagination";

const PostPreview = ({ entry, widgetFor }) => {
  const data = entry.get("data").toJS();

  const highlightRoot = useSyntaxHighlighter();

  const pagination: IPagination = {
    previous: {
      title: "Previous Post Title",
      href: ""
    },
    next: {
      title: "Next Post Title",
      href: ""
    }
  };

  return (
    <div ref={highlightRoot}>
      <BlogPostTemplate
        title={data.title || ""}
        date={data.date}
        category={data.category || ""}
        tags={data.tags || []}
        description={data.description || ""}
        hidden={data.hidden || false}
        githubRepository={data.githubRepository || null}
        pagination={pagination}
        body={() => widgetFor("body")}
        tableOfContents={() => <div className="text-center">Table Of Contents Placeholder</div>}
        showComments={false}
      />
    </div>
  );
};

export default PostPreview;
