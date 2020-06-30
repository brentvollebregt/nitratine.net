import React from "react";
import { Link } from "gatsby";
import { useSiteMetadata } from "../../../hooks/useSiteMetadata";

const getViewablePages = (
  current: number,
  pageCount: number,
  pagesEitherSideOfCurrentInPagination: number
) => {
  const minimum = 1;
  let length = 1 + pagesEitherSideOfCurrentInPagination * 2;
  if (length > pageCount) {
    length = pageCount;
  }
  let start = current - Math.floor(length / 2);
  start = Math.max(start, minimum);
  start = Math.min(start, minimum + pageCount - length);
  return Array.from({ length }, (_, i) => i + start);
};

export interface IPagination {
  current: number;
  pageCount: number;
  getPageRoute: (page: number) => string;
}

const Pagination: React.FC<IPagination> = ({ current, pageCount, getPageRoute }) => {
  const siteMetadata = useSiteMetadata();

  const isPreviousPage = current !== 1;
  const isNextPage = current < pageCount;

  const viewablePages = getViewablePages(
    current,
    pageCount,
    siteMetadata.blogFeed.pagesEitherSideOfCurrentInPagination
  );

  return (
    <nav className="text-center mb-5 mt-4">
      <ul className="pagination justify-content-center">
        <li className={`page-item ${isPreviousPage ? "" : "disabled"}`}>
          {isPreviousPage ? (
            <Link className="page-link" to={getPageRoute(current - 1)}>
              Previous
            </Link>
          ) : (
            <a className="page-link" tabIndex={-1}>
              Previous
            </a>
          )}
        </li>

        {viewablePages.map(page =>
          page === current ? (
            <li key={page} className="page-item active">
              <a className="page-link">
                {page} <span className="sr-only">(current)</span>
              </a>
            </li>
          ) : (
            <li key={page} className="page-item">
              <Link className="page-link" to={getPageRoute(page)}>
                {page}
              </Link>
            </li>
          )
        )}

        <li className={`page-item ${isNextPage ? "" : "disabled"}`}>
          {isNextPage ? (
            <Link className="page-link" to={getPageRoute(current + 1)}>
              Next
            </Link>
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
