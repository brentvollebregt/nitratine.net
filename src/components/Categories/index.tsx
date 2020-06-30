import React from "react";
import { Link } from "gatsby";
import { formatDate } from "../utils";

interface ICategories {
  categoryType: string;
  postsByCategory: IPostsByCategory[];
}

export interface IPostsByCategory {
  category: string;
  posts: {
    slug: string;
    title: string;
    date: Date;
    category: string;
    tags: string[];
  }[];
}

const Categories: React.FC<ICategories> = ({ categoryType, postsByCategory }) => (
  <>
    <h1 className="mb-4">Posts By {categoryType}</h1>

    {postsByCategory.map(c => (
      <div key={c.category}>
        <h2 id={c.category} className="mb-2 mt-3 category-title">
          {c.category}
        </h2>
        {c.posts
          .slice(0)
          .sort((p1, p2) => p2.date.valueOf() - p1.date.valueOf())
          .map(p => (
            <div key={p.slug}>
              <Link to={`/blog/archive/#${p.date.getFullYear()}`} className="mr-2 text-muted">
                {formatDate(p.date)}
              </Link>
              <Link to={p.slug}>{p.title}</Link>
              <Link to={`/blog/categories/#${p.category}`} className="badge badge-primary ml-2">
                {p.category}
              </Link>
              {p.tags.map(t => (
                <Link key={t} to={`/blog/tags/#${t}`} className="badge badge-warning ml-1">
                  {t}
                </Link>
              ))}
            </div>
          ))}
      </div>
    ))}
  </>
);

export default Categories;
