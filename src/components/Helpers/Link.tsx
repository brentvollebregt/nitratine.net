import React from "react";
import { Link as GatsbyLink } from "gatsby";
import { OutboundLink } from "gatsby-plugin-google-analytics";
import { isExternalPath } from "../utils";

interface ILink {
  href: string;
  className?: string;
  role?: string;
  title?: string;
}

const Link: React.FC<React.PropsWithChildren<ILink>> = ({
  children,
  href,
  className,
  role,
  title
}) => {
  const extras = { className, role, title };

  return isExternalPath(href) ? (
    <OutboundLink href={href} {...extras}>
      {children}
    </OutboundLink>
  ) : (
    <GatsbyLink to={href} {...extras}>
      {children}
    </GatsbyLink>
  );
};

export default Link;
