import React from "react";

const truncate = (string: string, maxLength: number) => {
  if (string.length <= maxLength) {
    return string;
  }
  return `${string.substring(0, maxLength)}...`;
};

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
    <nav className="blog-pagination text-center mb-5 mt-4">
      {previous !== undefined && (
        <a className="btn btn-outline-primary mt-1" href={previous.href}>
          &larr; {truncate(previous.title, 30)}
        </a>
      )}
      {next !== undefined && (
        <a className="btn btn-outline-primary mt-1" href={next.href}>
          {truncate(next.title, 30)} &rarr;
        </a>
      )}
    </nav>
  );
};

export default Pagination;
