import React from "react";
import staticConfig from "./src/config/static.json";

export const onPreRenderHTML = ({ getHeadComponents, replaceHeadComponents }) => {
  const headComponents = getHeadComponents();
  headComponents.push(
    <script key={"platform.js"} async src="https://apis.google.com/js/platform.js"></script>
  );
  if (staticConfig.adsense.enabled) {
    headComponents.push(
      <script
        data-ad-client={`ca-${staticConfig.adsense.publisherId}`}
        async
        src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
      ></script>
    );
  }
  replaceHeadComponents(headComponents);
};
