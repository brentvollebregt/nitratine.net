import React from "react";
import { graphql } from "gatsby";
import Base from "../../../components/Base";
import BlogBase from "../../../components/Blog/Base";
import Categories, { IPostsByCategory } from "../../../components/Categories";

const TagsPage = ({ data }) => {
  const rawCategories: CategoryFromQuery[] = data.allMarkdownRemark.group;
  const categories: IPostsByCategory[] = rawCategories.map(c => ({
    category: c.fieldValue,
    posts: c.edges.map(({ node }) => ({
      slug: node.fields.slug,
      title: node.frontmatter.title,
      date: new Date(node.frontmatter.date),
      category: node.frontmatter.category,
      tags: node.frontmatter.tags
    }))
  }));

  return (
    <Base>
      <BlogBase>
        <Categories categoryType="Tag" postsByCategory={categories} />
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
    allMarkdownRemark(limit: 1000) {
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
