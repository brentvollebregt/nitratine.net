import React, { useState } from "react";
import { useLocation } from "@reach/router";
import matchSorter from "match-sorter";
import usePostSummaries, { PostSummary } from "../../hooks/usePostSummaries";
import { formatDate } from "../utils";

const Search: React.FC = () => {
  const postSummaries = usePostSummaries();
  const location = useLocation();

  const queryInUrl =
    location.href !== undefined ? new URL(location.href).searchParams.get("q") ?? "" : "";
  const [query, setQuery] = useState(queryInUrl);

  const matches = matchSorter<PostSummary>(postSummaries, query, {
    keys: ["slug", "title", "category", "tags", "githubRepository", "description"]
  });

  return (
    <div>
      <h1 className="text-center">Local Nitratine.net Search</h1>

      <div className="input-group my-4">
        <input
          type="text"
          className="form-control text-center"
          placeholder="Search"
          aria-label="Search"
          value={query}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.currentTarget.value)}
        />
      </div>

      {query !== "" && (
        <div id="results">
          {matches.map(p => (
            <Match key={p.slug} post={p} />
          ))}
        </div>
      )}
    </div>
  );
};

const Match: React.FC<{ post: PostSummary }> = ({ post }) => {
  return (
    <div>
      <h3 className="mb-0">
        <a href={post.slug}>{post.title}</a>
      </h3>
      <p className="text-muted mb-0">
        <a className="text-muted" href={`/blog/archive/#${post.date.getFullYear()}`}>
          {formatDate(post.date)}
        </a>
        <a className="badge badge-primary ml-2" href="/blog/categories/#YouTube">
          {post.category}
        </a>
        {post.tags.map(t => (
          <a className="badge badge-warning ml-1" href={`/blog/tags/#${t}`}>
            {t}
          </a>
        ))}
      </p>
      <p>
        This is a Python keylogger which will work on Windows, Mac and Linux. This script uses the
        pynput module. This python keylogger will store typed keys in a file in order of when they
        were typed.
      </p>
    </div>
  );
};

export default Search;
