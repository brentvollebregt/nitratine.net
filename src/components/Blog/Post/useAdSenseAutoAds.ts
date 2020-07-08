import { useEffect } from "react";
import useStaticConfig from "../../../hooks/useStaticConfig";

// TODO REMOVE AFTER FINDING ANOTHER METHOD

const tagId = "adsense-script";

const useAdSenseAutoAds = () => {
  const { adsense: adsenseConfig } = useStaticConfig();

  useEffect(() => {
    if (adsenseConfig.enabled && document) {
      // Setup tag in head
      const adSenseScriptTag = document.createElement("script");
      adSenseScriptTag.id = tagId;
      adSenseScriptTag.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js";
      adSenseScriptTag.async = true;
      adSenseScriptTag.defer = true;
      adSenseScriptTag.setAttribute("data-ad-client", `ca-${adsenseConfig.publisherId}`);
      document.body.insertBefore(adSenseScriptTag, document.body.firstChild);
    }

    // Remove tag from head and remove ads on unmount
    () => {
      if (adsenseConfig.enabled && document) {
        const selectedAdSenseScriptTag = document.getElementById(tagId);
        if (selectedAdSenseScriptTag !== null) {
          selectedAdSenseScriptTag.remove();
        }

        Array.from(document.getElementsByClassName("google-auto-placed")).forEach(e => e.remove());
        Array.from(document.getElementsByClassName("adsbygoogle")).forEach(e => e.remove());
      }
    };
  }, []);
};

export default useAdSenseAutoAds;
