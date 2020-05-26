import React from "react";
import PropTypes from "prop-types";
import { kebabCase } from "lodash";
import { Helmet } from "react-helmet";
import { graphql, Link } from "gatsby";
import Base from "../components/Base";

export const BlogPostTemplate = ({ id, html, date, description, title, tags }) => {
  return <div>Blog Post Template</div>;
};

const BlogPost = ({ data }) => {
  const { id, html } = data.markdownRemark;
  const { date, title, description, tags } = data.markdownRemark.frontmatter;

  return (
    <Base>
      <BlogPostTemplate
        id={id}
        html={html}
        date={date}
        description={description}
        title={title}
        tags={tags}
      />
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
        date(formatString: "MMMM DD, YYYY")
        title
        description
        tags
      }
    }
  }
`;
