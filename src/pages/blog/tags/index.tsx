import React from "react";
import { Helmet } from "react-helmet";
import { Link, graphql } from "gatsby";

const TagsPage = ({}) => <div>Tags</div>;

export default TagsPage;

export const tagPageQuery = graphql`
  query TagsQuery {
    site {
      siteMetadata {
        title
      }
    }
    allMarkdownRemark(limit: 1000) {
      group(field: frontmatter___tags) {
        fieldValue
        totalCount
      }
    }
  }
`;
