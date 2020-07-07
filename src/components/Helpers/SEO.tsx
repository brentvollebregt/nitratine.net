import React from "react";
import { useLocation } from "@reach/router";
import { Helmet } from "react-helmet";
import { makeUriEndWithSlash } from "../utils";
import staticConfig from "../../config/static.json";

interface ISEO {
  title: string;
  description: string;
  relativeImagePath?: string;
  isPost?: boolean;
  noIndex?: boolean;
}

const SEO: React.FC<ISEO> = ({
  title,
  description,
  relativeImagePath = staticConfig.siteImage as string,
  isPost = false,
  noIndex = false
}) => {
  const location = useLocation();

  const relativePath = makeUriEndWithSlash(location.pathname);

  return (
    <Helmet>
      {/* Have to provide an alternate otherwise the tag sticks */}
      {noIndex ? <meta name="robots" content="noindex" /> : <meta name="robots" content="all" />}

      <title>
        {title !== "" ? `${title} - ` : ""}
        {staticConfig.title}
      </title>
      <link rel="canonical" href={`${staticConfig.baseUrl}${relativePath}`} />
      <meta name="description" content={description} />
      <meta name="image" content={`${staticConfig.baseUrl}${relativeImagePath}`} />

      <meta property="og:url" content={`${staticConfig.baseUrl}${relativePath}`} />
      <meta property="og:type" content={isPost ? "article" : "website"} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={`${staticConfig.baseUrl}${relativeImagePath}`} />

      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:creator" content={staticConfig.social.twitter} />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={`${staticConfig.baseUrl}${relativeImagePath}`} />
    </Helmet>
  );
};

export default SEO;