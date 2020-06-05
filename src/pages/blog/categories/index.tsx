import React from "react";
import { Helmet } from "react-helmet";
import { Link, graphql } from "gatsby";

const CategoriesPage = ({}) => <div>Categories</div>;

export default CategoriesPage;

export const categoryPageQuery = graphql`
  query CategoryQuery {
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
