import React from "react";
import Header, { IHeader } from "./Header";
import FeaturedPosts, { IFeaturedPosts } from "./FeaturedPosts";

export interface IHome extends IHeader, IFeaturedPosts {}

const Home: React.FC<IHome> = ({ image, leadText, buttons, featuredPosts }) => (
  <>
    <Header image={image} leadText={leadText} buttons={buttons} />
    {/* The Netlify preview passed an empty array, this is used the disable the following as we cannot get a list of posts */}
    {featuredPosts.length !== 0 && <FeaturedPosts featuredPosts={featuredPosts} />}
  </>
);

export default Home;
