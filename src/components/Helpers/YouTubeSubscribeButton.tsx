import React, { useEffect, useRef } from "react";

interface IYouTubeSubscribeButton {
  layout: "default" | "full";
}

const YouTubeSubscribeButton: React.FC<IYouTubeSubscribeButton> = ({ layout }) => {
  const tag = useRef<HTMLScriptElement>(null);

  useEffect(() => {
    if (document) {
      // Setup tag in head
      const scriptTag = document.createElement("script");
      scriptTag.src = "https://apis.google.com/js/platform.js";
      scriptTag.async = true;
      scriptTag.defer = true;
      document.body.insertBefore(scriptTag, document.body.firstChild);

      tag.current = scriptTag;
    }

    // Remove tag from head on unmount
    () => {
      if (document && tag.current !== null) {
        tag.current.remove();
      }
    };
  }, []);

  return (
    <div
      className="g-ytsubscribe"
      data-channel="PrivateSplat"
      data-layout={layout}
      data-count="default"
    />
  );
};

export default YouTubeSubscribeButton;
