import React from "react";

export const onPreRenderHTML = ({ getHeadComponents, replaceHeadComponents }) => {
  const headComponents = getHeadComponents();
  const headComponentsWithPlatformJs = headComponents.concat(
    <script key={"platform.js"} async src="https://apis.google.com/js/platform.js"></script>
  );
  replaceHeadComponents(headComponentsWithPlatformJs);
};
