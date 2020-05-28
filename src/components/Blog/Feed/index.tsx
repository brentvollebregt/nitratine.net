import React from "react";
import PostTile, { IPostTile } from "./PostTile";
import Pagination, { IPagination } from "./Pagination";

interface IFeed {
  posts: IPostTile[];
  pagination: IPagination;
}

const Feed: React.FC<IFeed> = ({ posts, pagination }) => (
  <div>
    <h1>Nitratine Blog Feed</h1>
    {posts.map(post => (
      <PostTile {...post} />
    ))}
    <Pagination {...pagination} />
  </div>
);

export default Feed;
