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

const BlogPost = ({ data }) => {
  // const { id, html } = data.markdownRemark;
  // const { title, date, category, tags, description } = data.markdownRemark.frontmatter;

  const posts: IPostTile[] = [];
  const pagination: IPagination = {
    previous: undefined,
    current: 1,
    next: undefined,
    visiblePages: [1],
    getPageRoute: (page: number) => (page === 1 ? `/blog` : `/blog/page${page}`)
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
  query BlogFeed($id: String!) {
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
