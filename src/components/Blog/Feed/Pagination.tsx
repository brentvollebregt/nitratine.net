import React from "react";

export interface IPagination {
  current: number;
  previous: number | undefined;
  next: number | undefined;
  visiblePages: number[];
  getPageRoute: (page: number) => string; // TODO Account for 1 => home
}

const Pagination: React.FC<IPagination> = ({
  current,
  previous,
  next,
  visiblePages,
  getPageRoute
}) => {
  return (
    <nav className="blog-pagination text-center mb-5 mt-4">
      <ul className="pagination justify-content-center">
        <li className={`page-item ${previous !== undefined ? "disabled" : ""}`}>
          {previous !== undefined ? (
            <a className="page-link" href={getPageRoute(previous)}>
              Previous
            </a>
          ) : (
            <a className="page-link" tabIndex={-1}>
              Previous
            </a>
          )}
        </li>

        {visiblePages.map(page =>
          page === current ? (
            <li className="page-item active">
              <a className="page-link" href="">
                {page} <span className="sr-only">(current)</span>
              </a>
            </li>
          ) : (
            <li className="page-item">
              <a className="page-link" href={getPageRoute(page)}>
                {page}
              </a>
            </li>
          )
        )}

        <li className={`page-item ${previous !== undefined ? "disabled" : ""}`}>
          {next !== undefined ? (
            <a className="page-link" href={getPageRoute(previous)}>
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
  );
};

export default Pagination;
