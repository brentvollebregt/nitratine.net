import React from "react";
import Header, { IHeader } from "./Header";
import FeaturedPosts from "./FeaturedPosts";

export interface IHome extends IHeader {}

const Home: React.FC<IHome> = ({ image, leadText, buttons }) => (
  <>
    <Header image={image} leadText={leadText} buttons={buttons} />
    <FeaturedPosts />
  </>
);

export default Home;
