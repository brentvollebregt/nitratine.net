import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import BlogBase from "../components/Blog/Base";
import { IPostTile } from "../components/Blog/Feed/PostTile";
import { IPagination } from "../components/Blog/Feed/Pagination";
import Feed from "../components/Blog/Feed";

interface IBlogFeedPageTemplate {
  posts: IPostTile[];
  pagination: IPagination;
}

export const BlogFeedPageTemplate: React.FC<IBlogFeedPageTemplate> = ({ posts, pagination }) => {
  return <Feed posts={posts} pagination={pagination} />;
};

const BlogPost = ({ data, pageContext }) => {
  const rawPosts = data.allMarkdownRemark.edges;

  const posts: IPostTile[] = rawPosts.map(p => ({
    title: p.node.frontmatter.title,
    href: p.node.fields.slug,
    date: new Date(p.node.frontmatter.date),
    category: p.node.frontmatter.category,
    tags: p.node.frontmatter.tags,
    description: p.node.frontmatter.description,
    thumbnailSrc: p.node.frontmatter.image.publicURL
  }));

  const pagination: IPagination = {
    current: pageContext.currentPage,
    pageCount: pageContext.numPages,
    getPageRoute: (page: number) => (page === 1 ? `/blog` : `/blog/page/${page}`)
  };

  console.log("pageContext", pageContext);

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
              publicURL
            }
          }
        }
      }
    }
  }
`;
