import React from "react";
import { graphql } from "gatsby";
import Base from "../../../components/Base";
import BlogBase from "../../../components/Blog/Base";
import Categories, { IPostsByCategory } from "../../../components/Categories";

const ArchivePage = ({ data }: { data: Query }) => {
  const posts = data.allMarkdownRemark.edges;
  const postsGroupedByYear = posts
    .reduce((acc, { node }) => {
      const post = {
        slug: node.fields.slug,
        title: node.frontmatter.title,
        date: new Date(node.frontmatter.date),
        category: node.frontmatter.category,
        tags: node.frontmatter.tags
      };
      const yearKey = post.date.getFullYear().toString();
      const currentYearKeyValue = acc.find(c => c.category === yearKey);
      const currentYearKeyPosts =
        currentYearKeyValue !== undefined ? currentYearKeyValue.posts : [];
      return [
        ...acc.filter(c => c.category !== yearKey),
        {
          category: yearKey,
          posts: [...currentYearKeyPosts, post]
        } as IPostsByCategory
      ];
    }, [] as IPostsByCategory[])
    .sort((c1, c2) => (c1.category > c2.category ? -1 : 1));

  return (
    <Base>
      <BlogBase>
        <Categories categoryType="Year" postsByCategory={postsGroupedByYear} />
      </BlogBase>
    </Base>
  );
};

export default ArchivePage;

interface Query {
  allMarkdownRemark: {
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
  };
}

export const categoryPageQuery = graphql`
  {
    allMarkdownRemark(filter: { frontmatter: { templateKey: { eq: "blog-post" } } }) {
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
`;
