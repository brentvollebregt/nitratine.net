import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import BlogBase from "../components/Blog/BlogBase";

interface IBlogPostTemplate {
  title: string;
  date: Date;
  category: string;
  tags: string[];
  description: string;
  body: React.FC;
}

export const BlogPostTemplate: React.FC<IBlogPostTemplate> = ({
  title,
  date,
  category,
  tags,
  description,
  body
}) => {
  return (
    <div>
      <h1>Blog Post Template</h1>
      <p>TODO: Title section</p>
      <p>TODO: GitHub link</p>
      <p>TODO: Post</p>
      <p>TODO: Previous / next</p>
      <p>TODO: Comments</p>
    </div>
  );
};

const BlogPost = ({ data }) => {
  const { title, date, category, tags, description } = data.markdownRemark.frontmatter;

  const body = () => <div dangerouslySetInnerHTML={{ __html: data.markdownRemark.html }} />;

  return (
    <Base>
      <BlogBase>
        <BlogPostTemplate
          title={title}
          date={date}
          category={category}
          tags={tags}
          description={description}
          body={body}
        />
      </BlogBase>
    </Base>
  );
};

export default BlogPost;

export const pageQuery = graphql`
  query BlogPostByID($id: String!) {
    markdownRemark(id: { eq: $id }) {
      id
      html
      frontmatter {
        title
        date
        category
        tags
        description
      }
    }
  }
`;
