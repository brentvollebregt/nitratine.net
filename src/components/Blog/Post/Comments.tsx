import React from "react";
import { useLocation } from "@reach/router";
import { Disqus } from "gatsby-plugin-disqus";
import { makeUriEndWithSlash } from "../../utils";
import useStaticConfig from "../../../hooks/useStaticConfig";

interface IComments {
  title: string;
  slug?: string;
}

const Comments: React.FC<IComments> = ({ title, slug }) => {
  const location = useLocation();
  const { siteUrl } = useStaticConfig();

  const relativePath = makeUriEndWithSlash(location.pathname);

  return !slug ? (
    <div className="text-center">Slug has not been provided so comments are disabled.</div>
  ) : (
    <Disqus
      config={{
        title,
        url: `${siteUrl}${relativePath}`,
        identifier: `${siteUrl}${relativePath}`
      }}
    />
  );
};

export default Comments;
