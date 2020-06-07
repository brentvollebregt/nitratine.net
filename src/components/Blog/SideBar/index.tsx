import React from "react";
import { useStaticQuery, graphql } from "gatsby";
import ReactMarkdown from "react-markdown";
import sideBarConfig from "../../../config/sidebar.json";
import "./SideBar.scss";
import { Helmet } from "react-helmet";

interface ICategories {
  name: string;
  postCount: number;
}

interface ICategoryPrefix {
  category: string;
  prefix: number;
}

interface IRecentVideos {
  thumbnailSrc: string;
  href: string;
}

interface IFeaturedSites {
  title: string;
  imageSrc: string;
  href: string;
}

const SideBar: React.FC = () => {
  const { allMarkdownRemark } = useStaticQuery(graphql`
    query SidebarQuery {
      allMarkdownRemark(filter: { frontmatter: { templateKey: { eq: "blog-post" } } }) {
        edges {
          node {
            frontmatter {
              category
            }
          }
        }
      }
    }
  `);

  const categoryOccurrences: string[] = allMarkdownRemark.edges.map(
    x => x.node.frontmatter.category
  );

  const about: string = sideBarConfig["about"];
  const categories: ICategories[] = categoryOccurrences
    .reduce((acc, category) => {
      const existing = acc.find(c => c.name === category);
      return [
        ...acc.filter(c => c.name !== category),
        existing !== undefined
          ? {
              name: category,
              postCount: existing.postCount + 1
            }
          : {
              name: category,
              postCount: 1
            }
      ];
    }, [] as ICategories[])
    .sort();
  const categoryPrefixes: ICategoryPrefix[] = sideBarConfig["categoryPrefixes"];
  const recentVideos: IRecentVideos[] = sideBarConfig["recentVideos"];
  const featuredSites: IFeaturedSites[] = sideBarConfig["featuredSites"];

  const getCategoryPrefix = (category: string) =>
    categoryPrefixes.find(c => c.category === category)?.prefix ?? "";

  return (
    <aside className="col-blog-sidebar blog-sidebar">
      <div className="card p-3 mb-3 bg-light about">
        <h4 className="text-center text-lg-left">About</h4>
        <ReactMarkdown source={about} />
      </div>

      <div className="input-group mb-3">
        <input
          id="search"
          type="text"
          className="form-control"
          placeholder="Search"
          aria-label="Search"
        />
        <div className="input-group-append">
          <button id="search-submit" className="btn btn-outline-primary" type="button">
            Search
          </button>
        </div>
      </div>

      <div className="card p-3 mb-3 bg-light">
        <h4 className="text-center text-lg-left">Categories</h4>
        <ol className="list-unstyled mb-0 text-center text-lg-left">
          {categories.map(({ name, postCount }) => (
            <li key={name}>
              <a href={`/blog/categories/#${name}`}>
                {getCategoryPrefix(name)} {name}
                <span className="badge badge-primary ml-3">{postCount}</span>
              </a>
            </li>
          ))}
        </ol>
      </div>

      <div className="card p-3 mb-3 bg-light">
        <h4 className="text-center text-lg-left">PyTutorials on YouTube</h4>
        <Helmet>
          <script src="https://apis.google.com/js/platform.js"></script>
        </Helmet>
        <div style={{ textAlign: "center" }}>
          <div
            className="g-ytsubscribe"
            data-channel="PrivateSplat"
            data-layout="full"
            data-count="default"
          ></div>
        </div>
      </div>

      <div className="card p-3 mb-3 bg-light">
        <h4 className="text-center text-lg-left">Recent Videos</h4>
        <div id="recent-yt-videos" className="yt_video_container">
          {recentVideos.map(({ thumbnailSrc, href }) => (
            <img
              key={thumbnailSrc}
              src={thumbnailSrc}
              onClick={() => window.open(href, "_blank")}
            />
          ))}
        </div>
      </div>

      <div className="card p-3 mb-3 bg-light">
        <h4 className="text-center text-lg-left">Featured Sites</h4>
        <div className="featured-sites">
          {featuredSites.map(({ title, imageSrc, href }) => (
            <a key={title} title={title} href={href}>
              <img src={imageSrc} className="mw-100" />
            </a>
          ))}
        </div>
      </div>
    </aside>
  );
};

export default SideBar;
