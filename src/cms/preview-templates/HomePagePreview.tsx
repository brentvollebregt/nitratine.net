import React from "react";
import { HomePageTemplate } from "../../templates/home-page";

const IndexPagePreview = ({ entry, getAsset }) => {
  const data = entry.get("data").toJS();
  // getAsset(data.image) // getAsset is beside entry
  return <HomePageTemplate image={data.image} leadText={data.leadText} buttons={data.buttons} />;
};

export default IndexPagePreview;
