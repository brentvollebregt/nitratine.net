import React from "react";
import Feed, { IFeed } from "./Feed";
import SideBar, { ISideBar } from "./SideBar";

interface IBlog extends IFeed, ISideBar {}

const Blog: React.FC<IBlog> = props => (
  <div className="row">
    <div className="col-blog-content blog-main">
      <h1 className="mb-4">Nitratine Blog Feed</h1>
      <Feed {...props} />
    </div>
    <SideBar {...props} />
  </div>
);

export default Blog;
