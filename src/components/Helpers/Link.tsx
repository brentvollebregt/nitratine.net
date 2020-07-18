import React from "react";
import { Link as GatsbyLink } from "gatsby";
import { useLocation } from "@reach/router";
import { OutboundLink } from "gatsby-plugin-google-analytics";
import useStaticConfig, { UseInternalLinkingOptions } from "../../hooks/useStaticConfig";
import { isExternalPath } from "../utils";

interface ILink {
  href: string;
  className?: string;
  role?: string;
  title?: string;
  forceExternal?: boolean;
}

const Link: React.FC<React.PropsWithChildren<ILink>> = ({
  children,
  href,
  className,
  role,
  title,
  forceExternal = false
}) => {
  const { pathname } = useLocation();
  const { useInternalLinking } = useStaticConfig();
  const extras = { className, role, title };

  if (isExternalPath(href) || forceExternal) {
    return (
      <OutboundLink href={href} {...extras}>
        {children}
      </OutboundLink>
    );
  }

  if (shouldForceExternalLink(useInternalLinking, href, pathname)) {
    return (
      <a href={href} {...extras}>
        {children}
      </a>
    );
  }

  return (
    <GatsbyLink to={href} {...extras}>
      {children}
    </GatsbyLink>
  );
};

const shouldForceExternalLink = (
  useInternalLinking: UseInternalLinkingOptions,
  href: string,
  pathname: string
) => {
  switch (useInternalLinking) {
    case "always":
      return false;
    case "never":
      return true;
    case "non-post-associations":
      return href.startsWith("/blog/post/") || pathname.startsWith("/blog/post/");
  }
};

export default Link;
