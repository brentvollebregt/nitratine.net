import React from "react";
import { BlogPostTemplate } from "../../templates/blog-post";
import ReactMarkdown from "react-markdown";

const PostPreview = ({ entry }) => {
  const data = entry.get("data").toJS();
  console.log("data", data);
  return (
    <BlogPostTemplate
      title={data.title || ""}
      date={data.date}
      category={data.category || ""}
      tags={data.tags || []}
      description={data.description || ""}
      hidden={data.hidden || false}
      githubRepository={data.githubRepository || null}
      body={() => <ReactMarkdown source={data.body || ""} />}
    />
  );
};

export default PostPreview;
