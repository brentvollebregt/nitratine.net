import React from "react";
import { formatDate } from "../../utils";
import "./PostTile.scss";

export interface IPostTile {
  title: string;
  href: string;
  date: Date;
  category: string[];
  tags: string[];
  description: string;
  thumbnailSrc: string;
}

const PostTile: React.FC<IPostTile> = ({
  title,
  href,
  date,
  category,
  tags,
  description,
  thumbnailSrc
}) => {
  return (
    <div className="card mb-4 blog-card">
      <div className="thumbnail-wrapper">
        <img className="thumbnail" alt="Thumbnail" src={thumbnailSrc} />
      </div>
      <div className="p-3">
        <h3 className="mb-0">
          <a className="text-dark" href={href}>
            {title}
          </a>
        </h3>
        <div className="mb-1">
          <a href={`/blog/archive/#${date.getFullYear()}`} className="text-muted">
            {formatDate(date)}
          </a>
          <a href={`/blog/categories/#${category}`} className="badge badge-primary ml-2 mr-1">
            {category}
          </a>
          {tags.map(tag => (
            <a href={`/blog/tags/#${tag}`} className="badge badge-warning mr-1">
              {tag}
            </a>
          ))}
        </div>
        <p className="card-text">{description}</p>
        <a href={href} role="button" className="btn btn-outline-primary btn-block">
          Read More →
        </a>
      </div>
    </div>
  );
};

export default PostTile;
