import React from "react";
import { Button } from "react-bootstrap";
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
        <Button variant="outline-primary" href={previous.href} className="mx-1 mt-1">
          &larr; {truncateString(previous.title, 30)}
        </Button>
      )}

      {next !== undefined && (
        <Button variant="outline-primary" href={next.href} className="mx-1 mt-1">
          {truncateString(next.title, 30)} &rarr;
        </Button>
      )}
    </nav>
  );
};

export default Pagination;
