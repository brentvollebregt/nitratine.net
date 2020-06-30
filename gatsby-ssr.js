import React from "react";

export const onPreRenderHTML = ({ getHeadComponents, replaceHeadComponents }) => {
  const headComponents = getHeadComponents();
  const headComponentsWithPlatformJs = headComponents.concat(
    <script async src="https://apis.google.com/js/platform.js"></script>
  );
  replaceHeadComponents(headComponentsWithPlatformJs);
  console.log(headComponentsWithPlatformJs[headComponentsWithPlatformJs.length - 1]);
};
