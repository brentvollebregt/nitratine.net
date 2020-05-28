import React from "react";
import { BlogPostTemplate } from "../../templates/blog-post";
import ReactMarkdown from "react-markdown";

const PostPreview = ({ entry }) => {
  const data = entry.get("data").toJS();
  return (
    <BlogPostTemplate
      title={data.title}
      date={data.date}
      category={data.category}
      tags={data.tags}
      description={data.description}
      hidden={data.hidden}
      githubRepository={data.githubRepository}
      body={() => <ReactMarkdown source={data.body} />}
    />
  );
};

export default PostPreview;
