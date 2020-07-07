import React from "react";
import { LocationProvider } from "@reach/router";
import { HomePageTemplate } from "../../templates/home-page";

const IndexPagePreview = ({ entry, getAsset }) => {
  const data = entry.get("data").toJS();
  return (
    <LocationProvider>
      <HomePageTemplate
        image={{ blob: getAsset(entry.getIn(["data", "image"])).url }}
        leadText={data.leadText}
        buttons={data.buttons}
        featuredPosts={[]}
      />
    </LocationProvider>
  );
};

export default IndexPagePreview;
