import React from "react";
import PostTile, { IPostTile } from "./PostTile";
import Pagination, { IPagination } from "./Pagination";
import SEO from "../../Helpers/SEO";

export interface IFeed {
  posts: IPostTile[];
  pagination: IPagination;
}

const Feed: React.FC<IFeed> = ({ posts, pagination }) => (
  <>
    <SEO
      title="Blog Feed"
      description="New posts and links with resources to my YouTube videos will appear here."
      noIndex={pagination.current !== 1}
    />

    <div>
      <h1 className="mb-4">Nitratine Blog Feed</h1>
      {posts.map(post => (
        <PostTile {...post} key={post.href} />
      ))}
      <Pagination {...pagination} />
    </div>
  </>
);

export default Feed;
