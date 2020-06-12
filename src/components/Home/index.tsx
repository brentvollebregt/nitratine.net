import React from "react";
import Header, { IHeader } from "./Header";
import FeaturedPosts, { IFeaturedPosts } from "./FeaturedPosts";

export interface IHome extends IHeader, IFeaturedPosts {}

const Home: React.FC<IHome> = ({ image, leadText, buttons, featuredPosts, postSummaries }) => (
  <>
    <Header image={image} leadText={leadText} buttons={buttons} />
    <FeaturedPosts featuredPosts={featuredPosts} postSummaries={postSummaries} />
  </>
);

export default Home;
