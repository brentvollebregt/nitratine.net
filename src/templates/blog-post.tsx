import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import BlogBase from "../components/Blog/Base";
import Header from "../components/Blog/Post/Header";
import Pagination, { IPagination } from "../components/Blog/Post/Pagination";
import Comments from "../components/Blog/Post/Comments";

interface IBlogPostTemplate {
  title: string;
  date: Date;
  category: string;
  tags: string[];
  hidden: boolean;
  githubRepository: string | null;
  description: string;
  body: React.FC;
}

export const BlogPostTemplate: React.FC<IBlogPostTemplate> = ({
  title,
  date,
  category,
  tags,
  hidden,
  githubRepository,
  description,
  body
}) => {
  const Body = body;
  return (
    <>
      <Header
        title={title}
        date={date}
        category={category}
        tags={tags}
        hidden={hidden}
        githubRepository={githubRepository}
        description={description}
      />

      <div className="post-content mt-3">
        <Body />
      </div>
    </>
  );
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

  const pagination: IPagination = {
    previous: undefined,
    next: undefined
  }; // TODO

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
        />
        <Pagination previous={pagination.previous} next={pagination.next} />
        <Comments />
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
