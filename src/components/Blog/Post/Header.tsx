import React from "react";
import { Link } from "gatsby";
import { formatDate } from "../../utils";
import GitHubLogoImage from "../../../img/github-icon.svg";
import "./Header.scss";

export interface IHeader {
  title: string;
  date: Date;
  category: string;
  tags: string[];
  hidden: boolean;
  githubRepository: string | null;
  description: string;
}

const Header: React.FC<IHeader> = ({
  title,
  date,
  category,
  tags,
  hidden,
  githubRepository,
  description
}) => {
  return (
    <div className="blog-post-header">
      <h1 className="blog-post-title">{title}</h1>

      <div className="mb-2">
        <Link to={`/blog/archive/#${date.getFullYear()}`} className="text-muted">
          {formatDate(date)}
        </Link>

        <Link to={`/blog/categories/#${category}`} className="badge badge-primary ml-2 mr-1">
          {category}
        </Link>

        {tags.map(tag => (
          <Link to={`/blog/tags/#${tag}`} className="badge badge-warning mr-1" key={tag}>
            {tag}
          </Link>
        ))}

        {hidden && <span className="badge badge-danger mr-1">Hidden</span>}

        <img
          src="https://hitcounter.pythonanywhere.com/count/tag.svg"
          alt="Hits"
          className="post-hits"
        />
      </div>

      <p className="lead">{description}</p>

      <hr className="mt-3 mb-0" />

      {githubRepository !== null && (
        <>
          <div className="github-summary py-3 d-block text-center">
            <a className="repo-name stretched-link" href={`https://github.com/${githubRepository}`}>
              <img src={(GitHubLogoImage as unknown) as string} alt="GitHub Icon" />
              <span className="ml-2">{githubRepository}</span>
            </a>

            <div className="repo-stats">
              <img
                alt="GitHub stars"
                src={`https://img.shields.io/github/stars/${githubRepository}?style=social`}
                className="mr-1"
              />
              <img
                alt="GitHub forks"
                src={`https://img.shields.io/github/forks/${githubRepository}?style=social`}
                className="mr-1"
              />
              <img
                alt="GitHub top language"
                src={`https://img.shields.io/github/languages/top/${githubRepository}`}
              />
            </div>
          </div>
          <hr className="my-0" />
        </>
      )}
    </div>
  );
};

export default Header;
