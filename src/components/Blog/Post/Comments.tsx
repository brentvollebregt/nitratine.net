import React from "react";
import { useLocation } from "@reach/router";
import { Disqus } from "gatsby-plugin-disqus";
import { makeUriEndWithSlash } from "../../utils";
import staticConfig from "../../../config/static.json";

interface IComments {
  title: string;
  slug?: string;
}

const Comments: React.FC<IComments> = ({ title, slug }) => {
  const location = useLocation();

  const relativePath = makeUriEndWithSlash(location.pathname);

  return !slug ? (
    <div className="text-center">Slug has not been provided so comments are disabled.</div>
  ) : (
    <Disqus
      config={{
        title,
        url: `${staticConfig.siteUrl}${relativePath}`,
        identifier: `${staticConfig.siteUrl}${relativePath}`
      }}
    />
  );
};

export default Comments;
