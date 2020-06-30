import { useEffect } from "react";
import adSenseConfig from "../../../config/adsense.json";

const tagId = "adsense-script";

const useAdSenseAutoAds = () => {
  useEffect(() => {
    if (adSenseConfig.enabled && document) {
      // Setup tag in head
      const adSenseScriptTag = document.createElement("script");
      adSenseScriptTag.id = tagId;
      adSenseScriptTag.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js";
      adSenseScriptTag.async = true;
      adSenseScriptTag.defer = true;
      adSenseScriptTag.setAttribute("data-ad-client", `ca-${adSenseConfig.publisherId}`);
      document.body.insertBefore(adSenseScriptTag, document.body.firstChild);
    }

    // Remove tag from head and remove ads on unmount
    () => {
      if (adSenseConfig.enabled && document) {
        const selectedAdSenseScriptTag = document.getElementById(tagId);
        if (selectedAdSenseScriptTag !== null) {
          selectedAdSenseScriptTag.remove();
        }

        Array.from(document.getElementsByClassName("google-auto-placed")).forEach(e => e.remove());
      }
    };
  }, []);
};

export default useAdSenseAutoAds;
