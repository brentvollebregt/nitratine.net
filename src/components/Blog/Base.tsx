import React from "react";
import SideBar from "./SideBar";
import "./Base.scss";

interface IBase {
  children: React.ReactNode;
}

const Base: React.FC<IBase> = ({ children }) => (
  <div className="row mb-4">
    <div className="col-blog-content blog-main">{children}</div>
    <SideBar />
  </div>
);

export default Base;
