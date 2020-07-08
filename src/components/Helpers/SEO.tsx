import React from "react";
import { useLocation } from "@reach/router";
import { Helmet } from "react-helmet";
import { makeUriEndWithSlash } from "../utils";
import useStaticConfig from "../../hooks/useStaticConfig";

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
  relativeImagePath,
  isPost = false,
  noIndex = false
}) => {
  const location = useLocation();
  const { siteUrl, title: siteTitle, siteImage, social } = useStaticConfig();

  const relativePath = makeUriEndWithSlash(location.pathname);
  const relativeImagePathWithFallback = relativeImagePath ?? siteImage;

  return (
    <Helmet>
      {/* Have to provide an alternate otherwise the tag sticks */}
      {noIndex ? <meta name="robots" content="noindex" /> : <meta name="robots" content="all" />}

      <title>
        {title !== "" ? `${title} - ` : ""}
        {siteTitle}
      </title>
      <link rel="canonical" href={`${siteUrl}${relativePath}`} />
      <meta name="description" content={description} />
      <meta name="image" content={`${siteUrl}${relativeImagePathWithFallback}`} />

      <meta property="og:url" content={`${siteUrl}${relativePath}`} />
      <meta property="og:type" content={isPost ? "article" : "website"} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={`${siteUrl}${relativeImagePathWithFallback}`} />

      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:creator" content={social.twitter} />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={`${siteUrl}${relativeImagePathWithFallback}`} />
    </Helmet>
  );
};

export default SEO;
