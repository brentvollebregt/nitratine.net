import React from "react";
import { Container } from "react-bootstrap";
import Link from "../Helpers/Link";
import rssImage from "../../img/rss-icon.svg";
import githubImage from "../../img/github-icon.svg";
import youtubeImage from "../../img/youtube-icon.svg";

const Footer: React.FC = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="footer bg-dark py-4 px-1">
      <Container>
        <div className="d-flex justify-content-center">
          <div className="top-group">
            <div className="link-group">
              <p className="header">Navigate</p>
              <Link href="/">Home</Link>
              <Link href="/blog/">Blog</Link>
              <Link href="/blog/categories/" className="ml-2">
                Categories
              </Link>
              <Link href="/blog/tags/" className="ml-2">
                Tags
              </Link>
              <Link href="/blog/archive/" className="ml-2">
                Archive
              </Link>
              <Link href="/portfolio/">Portfolio</Link>
              <Link href="/about/">About</Link>
            </div>

            <div className="link-group">
              <p className="header">Popular Projects</p>
              <Link href="/blog/post/auto-py-to-exe/">auto-py-to-exe</Link>
              <Link href="/blog/post/hit-counter/">hit-counter</Link>
              <Link href="/blog/post/whos-on-my-network/" forceExternal={true}>
                whos-on-my-network
              </Link>
              <Link href="/blog/post/monopoly-money/" forceExternal={true}>
                monopoly-money
              </Link>
            </div>

            <div className="link-group">
              <p className="header">Follow</p>
              <Link href="https://github.com/brentvollebregt" className="with-icon">
                <img src={githubImage} alt="GitHub Logo" style={{ filter: "invert(1)" }} />
                GitHub
              </Link>
              <Link href="https://www.youtube.com/c/PyTutorials" className="with-icon">
                <img src={youtubeImage} alt="YouTube Logo" />
                YouTube
              </Link>
              <Link href="/rss.xml" forceExternal={true} className="with-icon">
                <img src={rssImage} alt="RSS Logo" />
                Nitratine RSS Feed
              </Link>
            </div>
          </div>
        </div>

        <div className="mx-4">
          <hr />
        </div>

        <p className="text-center m-0">
          <small>© {year} Brent Vollebregt</small>
        </p>
      </Container>
    </footer>
  );
};
export default Footer;
