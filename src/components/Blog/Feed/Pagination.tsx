import React from "react";
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
    <nav className="blog-pagination text-center mb-5 mt-4">
      <ul className="pagination justify-content-center">
        <li className={`page-item ${isPreviousPage ? "" : "disabled"}`}>
          {isPreviousPage ? (
            <a className="page-link" href={getPageRoute(current - 1)}>
              Previous
            </a>
          ) : (
            <a className="page-link" tabIndex={-1}>
              Previous
            </a>
          )}
        </li>

        {viewablePages.map(page =>
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

        <li className={`page-item ${isNextPage ? "" : "disabled"}`}>
          {isNextPage ? (
            <a className="page-link" href={getPageRoute(current + 1)}>
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
