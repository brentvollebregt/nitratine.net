import React from "react";
import Header, { IHeader } from "./Header";
import Comments from "./Comments";
import Pagination, { IPagination } from "./Pagination";
import SEO from "../../Helpers/SEO";
import "./Post.scss";

export interface IPost extends IHeader {
  pagination: IPagination;
  body: React.FC;
  tableOfContents: React.FC | null;
  showComments: boolean;
  relativeImagePath: string;
  slug?: string;
}

const Post: React.FC<IPost> = ({
  title,
  date,
  category,
  tags,
  hidden,
  githubRepository,
  description,
  pagination,
  body,
  tableOfContents,
  showComments,
  relativeImagePath,
  slug
}) => {
  const Body = body;
  const TableOfContents = tableOfContents;

  return (
    <>
      <SEO
        title={title}
        description={description}
        relativeImagePath={relativeImagePath}
        isPost={true}
        noIndex={hidden}
      />

      <div className="blog-post">
        <Header
          title={title}
          date={date}
          category={category}
          tags={tags}
          hidden={hidden}
          githubRepository={githubRepository}
          description={description}
        />

        <div className="mt-3">
          {TableOfContents !== null && (
            <>
              <div className="toc">
                <TableOfContents />
              </div>
              <hr className="my-3" />
            </>
          )}

          <div className="body">
            <Body />
          </div>
        </div>

        <div className="mt-5">
          <Pagination previous={pagination.previous} next={pagination.next} />
        </div>

        {showComments && (
          <div className="mt-5">
            <Comments title={title} slug={slug} />
          </div>
        )}
      </div>
    </>
  );
};

export default Post;
