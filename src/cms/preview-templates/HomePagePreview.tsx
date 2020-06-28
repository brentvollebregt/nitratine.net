import React from "react";
import { HomePageTemplate } from "../../templates/home-page";

const IndexPagePreview = ({ entry, getAsset }) => {
  const data = entry.get("data").toJS();
  return (
    <HomePageTemplate
      image={{ blob: getAsset(entry.getIn(["data", "image"])).url }}
      leadText={data.leadText}
      buttons={data.buttons}
      featuredPosts={[]}
    />
  );
};

export default IndexPagePreview;
