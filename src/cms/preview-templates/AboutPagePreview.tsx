import React from "react";
import ReactMarkdown from "react-markdown";
import { AboutPageTemplate } from "../../templates/about-page";

const AboutPagePreview = ({ entry }) => {
  const data = entry.get("data").toJS();

  return (
    <AboutPageTemplate
      email={data.email}
      experience={data.experience}
      body={() => <ReactMarkdown source={data.body} />}
    />
  );
};

export default AboutPagePreview;
