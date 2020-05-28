import React from "react";
import SideBar from "./SideBar";
import "./BlogBase.scss";

interface IBlog {
  children: React.ReactNode;
}

const Blog: React.FC<IBlog> = ({ children }) => (
  <div className="row">
    <div className="col-blog-content blog-main">{children}</div>
    <SideBar />
  </div>
);

export default Blog;
