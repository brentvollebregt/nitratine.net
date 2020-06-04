import React from "react";
import { truncateString } from "../../utils";

interface PaginationSummary {
  title: string;
  href: string;
}

export interface IPagination {
  previous: PaginationSummary | undefined;
  next: PaginationSummary | undefined;
}

const Pagination: React.FC<IPagination> = ({ previous, next }) => {
  return (
    <nav className="text-center">
      {previous !== undefined && (
        <a className="btn btn-outline-primary" href={previous.href}>
          &larr; {truncateString(previous.title, 30)}
        </a>
      )}

      {next !== undefined && (
        <a className="btn btn-outline-primary ml-1" href={next.href}>
          {truncateString(next.title, 30)} &rarr;
        </a>
      )}
    </nav>
  );
};

export default Pagination;
