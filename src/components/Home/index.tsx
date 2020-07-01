import React from "react";
import Header, { IHeader } from "./Header";
import FeaturedPosts, { IFeaturedPosts } from "./FeaturedPosts";
import SEO from "../Helpers/SEO";

export interface IHome extends IHeader, IFeaturedPosts {}

const Home: React.FC<IHome> = ({ image, leadText, buttons, featuredPosts }) => (
  <>
    <SEO
      title=""
      description="A place where I share projects developed by me and tutorials on topics that I'm interested in. I own the PyTutorials YouTube channel and am the creator of auto-py-to-exe."
      relativePath="/"
    />

    <Header image={image} leadText={leadText} buttons={buttons} />
    {/* The Netlify preview passed an empty array, this is used the disable the following as we cannot get a list of posts */}
    {featuredPosts.length !== 0 && <FeaturedPosts featuredPosts={featuredPosts} />}
  </>
);

export default Home;
