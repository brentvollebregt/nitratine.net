import React from "react";

export interface IFeed {
  posts: {
    title: string;
    href: string;
    date: Date;
    category: string[];
    tags: string[];
    description: string;
    thumbnailSrc: string;
  }[];
  pagination: {
    current: number;
    previous: number | undefined;
    next: number | undefined;
    visiblePages: number[];
    getPageRoute: (page: number) => string; // TODO Account for 1 => home
  };
}

const Feed: React.FC<IFeed> = ({ posts, pagination }) => (
  <>
    {/* Posts */}
    {posts.map(({ title, href, date, category, tags, description, thumbnailSrc }) => (
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
              {date.toISOString()}
            </a>
            <a href={`/blog/categories/#${category}`} className="badge badge-primary ml-2">
              {category}
            </a>
            {tags.map(tag => (
              <a href={`/blog/tags/#${tag}`} className="badge badge-warning">
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
    ))}

    {/* Pagination */}

    <nav className="blog-pagination text-center mb-5 mt-4">
      <ul className="pagination justify-content-center">
        <li className={`page-item ${pagination.previous !== undefined ? "disabled" : ""}`}>
          {pagination.previous !== undefined ? (
            <a className="page-link" href={pagination.getPageRoute(pagination.previous)}>
              Previous
            </a>
          ) : (
            <a className="page-link" tabIndex={-1}>
              Previous
            </a>
          )}
        </li>

        {pagination.visiblePages.map(page =>
          page === pagination.current ? (
            <li className="page-item active">
              <a className="page-link" href="">
                {page} <span className="sr-only">(current)</span>
              </a>
            </li>
          ) : (
            <li className="page-item">
              <a className="page-link" href={pagination.getPageRoute(page)}>
                {page}
              </a>
            </li>
          )
        )}

        <li className={`page-item ${pagination.previous !== undefined ? "disabled" : ""}`}>
          {pagination.next !== undefined ? (
            <a className="page-link" href={pagination.getPageRoute(pagination.previous)}>
              Next
            </a>
          ) : (
            <a className="page-link" tabIndex={-1}>
              Next
            </a>
          )}
        </li>
      </ul>
    </nav>
  </>
);

export default Feed;
