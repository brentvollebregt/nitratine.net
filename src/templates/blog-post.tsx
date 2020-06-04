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
  const title: string = data.markdownRemark.frontmatter.title;
  const date = new Date(data.markdownRemark.frontmatter.date);
  const category: string = data.markdownRemark.frontmatter.category;
  const tags: string[] = data.markdownRemark.frontmatter.tags;
  const hidden: boolean = data.markdownRemark.frontmatter.hidden;
  const githubRepository: string | null = data.markdownRemark.frontmatter.githubRepository;
  const description: string = data.markdownRemark.frontmatter.description;

  const body = () => <div dangerouslySetInnerHTML={{ __html: data.markdownRemark.html }} />;
  const tableOfContents = () => (
    <div dangerouslySetInnerHTML={{ __html: data.markdownRemark.tableOfContents }} />
  );

  const pagination: IPagination = {
    previous: undefined,
    next: undefined
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
    markdownRemark(id: { eq: $id }) {
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
  }
`;
