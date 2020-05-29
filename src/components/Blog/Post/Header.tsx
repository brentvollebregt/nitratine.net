import React from "react";

interface IHeader {
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
    <>
      <h1 className="blog-post-title">{title}</h1>
      <div className="mb-3">
        <a href={`/blog/archive/${date.getFullYear()}`} className="text-muted">
          {date.toISOString()}
        </a>
        <a href={`/blog/categories/${category}`} className="badge badge-primary ml-2">
          {category}
        </a>
        {tags.map(tag => (
          <a href={`/blog/tags/${tag}`} className="badge badge-warning" key={tag}>
            {tag}
          </a>
        ))}
        {hidden && <span className="badge badge-danger">Hidden</span>}
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
            <a className="repo-name stretched-link" href="{{ github_repo.html_url }}">
              <img src="/assets/img/github-icon.png" alt="GitHub Icon" />
              <span className="ml-2">{githubRepository}</span>
            </a>

            <div className="repo-stats">
              <img
                alt="GitHub stars"
                src={`https://img.shields.io/github/stars/${githubRepository}?style=social`}
              />
              <img
                alt="GitHub forks"
                src={`https://img.shields.io/github/forks/${githubRepository}?style=social`}
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
    </>
  );
};

export default Header;
