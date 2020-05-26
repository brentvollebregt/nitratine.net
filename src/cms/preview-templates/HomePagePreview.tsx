import React from "react";
import { HomePageTemplate } from "../../templates/home-page";

const IndexPagePreview = ({ entry }) => {
  const data = entry.get("data").toJS();
  return <HomePageTemplate image={data.image} leadText={data.leadText} buttons={data.buttons} />;
};

export default IndexPagePreview;
