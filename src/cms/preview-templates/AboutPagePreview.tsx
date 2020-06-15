import React from "react";
import { AboutPageTemplate } from "../../templates/about-page";

const AboutPagePreview = ({ entry, widgetFor }) => {
  const data = entry.get("data").toJS();
  return (
    <AboutPageTemplate
      email={data.email}
      experience={data.experience}
      body={() => widgetFor("body")}
    />
  );
};

export default AboutPagePreview;
