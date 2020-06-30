import React from "react";
import { Link } from "gatsby";
import Img, { FluidObject } from "gatsby-image";
import { formatDate } from "../../utils";
import "./PostTile.scss";

export interface IPostTile {
  title: string;
  href: string;
  date: Date;
  category: string[];
  tags: string[];
  description: string;
  image: {
    childImageSharp: {
      fluid: FluidObject;
    };
  };
}

const PostTile: React.FC<IPostTile> = ({
  title,
  href,
  date,
  category,
  tags,
  description,
  image
}) => {
  return (
    <div className="card mb-4 blog-card">
      <div className="thumbnail-wrapper">
        <Img
          fluid={image.childImageSharp.fluid}
          alt={`${title} Thumbnail`}
          imgStyle={{
            objectFit: "cover"
          }}
          style={{ height: "100%" }}
        />
      </div>
      <div className="p-3">
        <h3 className="mb-0">
          <Link className="text-dark" to={href}>
            {title}
          </Link>
        </h3>
        <div className="mb-1">
          <Link to={`/blog/archive/#${date.getFullYear()}`} className="text-muted">
            {formatDate(date)}
          </Link>
          <Link to={`/blog/categories/#${category}`} className="badge badge-primary ml-2 mr-1">
            {category}
          </Link>
          {tags.map(tag => (
            <Link key={tag} to={`/blog/tags/#${tag}`} className="badge badge-warning mr-1">
              {tag}
            </Link>
          ))}
        </div>
        <p className="card-text">{description}</p>
        <Link to={href} role="button" className="btn btn-outline-primary btn-block">
          Read More →
        </Link>
      </div>
    </div>
  );
};

export default PostTile;
