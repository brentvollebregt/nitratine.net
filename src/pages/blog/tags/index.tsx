import React from "react";
import { graphql } from "gatsby";
import Base from "../../../components/Base";
import BlogBase from "../../../components/Blog/Base";
import Categories, { IPostsByCategory } from "../../../components/Categories";

const TagsPage = ({ data }) => {
  const rawTags: CategoryFromQuery[] = data.allMarkdownRemark.group;
  const postsGroupedByTags: IPostsByCategory[] = rawTags
    .map(c => ({
      category: c.fieldValue,
      posts: c.edges.map(({ node }) => ({
        slug: node.fields.slug,
        title: node.frontmatter.title,
        date: new Date(node.frontmatter.date),
        category: node.frontmatter.category,
        tags: node.frontmatter.tags
      }))
    }))
    .sort((c1, c2) => (c1.category > c2.category ? 1 : -1));

  return (
    <Base>
      <BlogBase>
        <Categories categoryType="Tag" postsByCategory={postsGroupedByTags} />
      </BlogBase>
    </Base>
  );
};

export default TagsPage;

interface CategoryFromQuery {
  fieldValue: string;
  edges: {
    node: {
      fields: {
        slug: string;
      };
      frontmatter: {
        title: string;
        date: string;
        category: string;
        tags: string[];
      };
    };
  }[];
}

export const pageQuery = graphql`
  {
    allMarkdownRemark(filter: { frontmatter: { templateKey: { eq: "blog-post" } } }) {
      group(field: frontmatter___tags) {
        fieldValue
        edges {
          node {
            fields {
              slug
            }
            frontmatter {
              title
              date
              category
              tags
            }
          }
        }
      }
    }
  }
`;
