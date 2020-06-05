import React from "react";
import { Helmet } from "react-helmet";
import { Link, graphql } from "gatsby";

const ArchivePage = ({}) => <div>Archive</div>;

export default ArchivePage;

export const categoryPageQuery = graphql`
  query ArchiveQuery {
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
