import React from "react";

// TODO Break into smaller components

interface ICategories {
  name: string;
  postCount: number;
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
  const categories: ICategories[] = [];
  const recentVideos: IRecentVideos[] = [];
  const featuredSites: IFeaturedSites[] = [];

  return (
    <aside className="col-blog-sidebar blog-sidebar">
      <div className="card p-3 mb-3 bg-light">
        <h4 className="text-center text-lg-left">About</h4>
        <p className="mb-0">
          Owner of <a href="https://www.youtube.com/PyTutorials">PyTutorials</a> and creator of
          <a href="https://github.com/brentvollebregt/auto-py-to-exe">auto-py-to-exe</a>. I enjoy
          making quick tutorials for people new to particular topics in Python and tools that help
          fix small things.
        </p>
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
            <li>
              <a href={`/blog/categories/#${name}`}>
                {name}
                <span className="badge badge-primary ml-3">{postCount}</span>
              </a>
            </li>
          ))}
        </ol>
      </div>

      <div className="card p-3 mb-3 bg-light">
        <h4 className="text-center text-lg-left">PyTutorials on YouTube</h4>
        <script src="https://apis.google.com/js/platform.js"></script>
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
            <img src={thumbnailSrc} onClick={() => window.open(href, "_blank")} />
          ))}
        </div>
      </div>

      <div className="card p-3 mb-3 bg-light">
        <h4 className="text-center text-lg-left">Featured Sites</h4>
        <div className="featured-sites">
          {featuredSites.map(({ title, imageSrc, href }) => (
            <a title={title} href={href}>
              <img src={imageSrc} />
            </a>
          ))}
        </div>
      </div>
    </aside>
  );
};

export default SideBar;
