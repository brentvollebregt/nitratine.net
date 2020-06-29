import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import BlogBase from "../components/Blog/Base";
import { IPostTile } from "../components/Blog/Feed/PostTile";
import { IPagination } from "../components/Blog/Feed/Pagination";
import Feed, { IFeed } from "../components/Blog/Feed";

export const BlogFeedPageTemplate: React.FC<IFeed> = props => {
  return <Feed {...props} />;
};

const BlogPost = ({ data, pageContext }) => {
  const rawPosts = data.allMarkdownRemark.edges;

  const posts: IPostTile[] = rawPosts.map(({ node }) => ({
    title: node.frontmatter.title,
    href: node.fields.slug,
    date: new Date(node.frontmatter.date),
    category: node.frontmatter.category,
    tags: node.frontmatter.tags,
    description: node.frontmatter.description,
    image: node.frontmatter.image
  }));

  const pagination: IPagination = {
    current: pageContext.currentPage,
    pageCount: pageContext.numPages,
    getPageRoute: (page: number) => (page === 1 ? `/blog` : `/blog/page/${page}`)
  };

  return (
    <Base>
      <BlogBase>
        <BlogFeedPageTemplate posts={posts} pagination={pagination} />
      </BlogBase>
    </Base>
  );
};

export default BlogPost;

export const pageQuery = graphql`
  query BlogFeed($skip: Int!, $limit: Int!) {
    allMarkdownRemark(
      sort: { fields: [frontmatter___date], order: DESC }
      filter: { frontmatter: { templateKey: { eq: "blog-post" }, hidden: { eq: false } } }
      limit: $limit
      skip: $skip
    ) {
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
            description
            image {
              childImageSharp {
                fluid(maxWidth: 2048, quality: 100) {
                  ...GatsbyImageSharpFluid
                }
              }
            }
          }
        }
      }
    }
  }
`;
