import React, { useEffect } from "react";

interface IYouTubeSubscribeButton {
  layout: "default" | "full";
}

const YouTubeSubscribeButton: React.FC<IYouTubeSubscribeButton> = ({ layout }) => {
  // If the GAPI has loaded, call it to create the subscribe button
  useEffect(() => {
    if ((window as any).gapi) {
      (window as any).gapi.ytsubscribe.go();
    }
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
