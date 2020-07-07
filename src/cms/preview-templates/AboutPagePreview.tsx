import React from "react";
import { LocationProvider } from "@reach/router";
import { AboutPageTemplate } from "../../templates/about-page";

const AboutPagePreview = ({ entry, widgetFor }) => {
  const data = entry.get("data").toJS();
  return (
    <LocationProvider>
      <AboutPageTemplate
        email={data.email}
        experience={data.experience}
        body={() => widgetFor("body")}
      />
    </LocationProvider>
  );
};

export default AboutPagePreview;
