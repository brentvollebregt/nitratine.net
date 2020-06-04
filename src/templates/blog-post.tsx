import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import BlogBase from "../components/Blog/Base";
import Post, { IPost } from "../components/Blog/Post";
import { IPagination } from "../components/Blog/Post/Pagination";

export const BlogPostTemplate: React.FC<IPost> = props => {
  return <Post {...props} />;
};

const BlogPost = ({ data }) => {
  const title: string = data.post.frontmatter.title;
  const date = new Date(data.post.frontmatter.date);
  const category: string = data.post.frontmatter.category;
  const tags: string[] = data.post.frontmatter.tags;
  const hidden: boolean = data.post.frontmatter.hidden;
  const githubRepository: string | null = data.post.frontmatter.githubRepository;
  const description: string = data.post.frontmatter.description;

  const body = () => <div dangerouslySetInnerHTML={{ __html: data.post.html }} />;
  const tableOfContents = () => (
    <div dangerouslySetInnerHTML={{ __html: data.post.tableOfContents }} />
  );

  // Pagination
  const id: string = data.post.id;
  const postSummaries = data.allPosts.edges;
  const postIndex: number = postSummaries.findIndex(x => x.node.id === id);

  const pagination: IPagination = {
    previous:
      postIndex - 1 === -1
        ? undefined
        : {
            title: postSummaries[postIndex - 1].node.frontmatter.title,
            href: postSummaries[postIndex - 1].node.fields.slug
          },
    next:
      postIndex + 1 === postSummaries.length
        ? undefined
        : {
            title: postSummaries[postIndex + 1].node.frontmatter.title,
            href: postSummaries[postIndex + 1].node.fields.slug
          }
  };

  return (
    <Base>
      <BlogBase>
        <BlogPostTemplate
          title={title}
          date={date}
          category={category}
          tags={tags}
          hidden={hidden}
          githubRepository={githubRepository}
          description={description}
          body={body}
          tableOfContents={tableOfContents}
          pagination={pagination}
          showComments={true}
        />
      </BlogBase>
    </Base>
  );
};

export default BlogPost;

export const pageQuery = graphql`
  query BlogPostByID($id: String!) {
    post: markdownRemark(id: { eq: $id }) {
      id
      html
      tableOfContents
      frontmatter {
        title
        date
        category
        tags
        hidden
        githubRepository
        description
      }
    }
    allPosts: allMarkdownRemark(
      filter: { frontmatter: { templateKey: { eq: "blog-post" } } }
      sort: { order: ASC, fields: [frontmatter___date] }
    ) {
      edges {
        node {
          id
          frontmatter {
            title
          }
          fields {
            slug
          }
        }
      }
    }
  }
`;
