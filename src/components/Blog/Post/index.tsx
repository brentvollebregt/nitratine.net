import React from "react";
import Header, { IHeader } from "./Header";
import Pagination, { IPagination } from "./Pagination";
import Comments from "./Comments";
import "./Post.scss";

export interface IPost extends IHeader {
  pagination: IPagination;
  body: React.FC;
  tableOfContents: React.FC | null;
  showComments: boolean;
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
  showComments
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

      <div className="mt-3">
        {TableOfContents !== null && (
          <>
            <div className="toc">
              <TableOfContents />
            </div>
            <hr className="my-3" />
          </>
        )}
        <Body />
      </div>

      <div className="mt-5">
        <Pagination previous={pagination.previous} next={pagination.next} />
      </div>
      {showComments && (
        <div className="mt-5">
          <Comments />
        </div>
      )}
    </>
  );
};

export default Post;
