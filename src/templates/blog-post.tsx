import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import BlogBase from "../components/Blog/Base";
import Header from "../components/Blog/Post/Header";
import Pagination, { IPagination } from "../components/Blog/Post/Pagination";
import Comments from "../components/Blog/Post/Comments";
import "../components/Blog/Post/Post.scss";

interface IBlogPostTemplate {
  title: string;
  date: Date;
  category: string;
  tags: string[];
  hidden: boolean;
  githubRepository: string | null;
  description: string;
  body: React.FC;
  tableOfContents: React.FC;
}

export const BlogPostTemplate: React.FC<IBlogPostTemplate> = ({
  title,
  date,
  category,
  tags,
  hidden,
  githubRepository,
  description,
  body,
  tableOfContents
}) => {
  const Body = body;
  const TableOfContents = tableOfContents;
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
        <div className="toc">
          <TableOfContents />
        </div>
        <hr className="my-3" />
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
  const tableOfContents = () => (
    <div dangerouslySetInnerHTML={{ __html: data.markdownRemark.tableOfContents }} />
  );

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
          tableOfContents={tableOfContents}
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
