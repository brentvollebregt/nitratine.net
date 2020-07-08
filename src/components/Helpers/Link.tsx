import React from "react";
import { Link as GatsbyLink } from "gatsby";
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
    <a href={href} {...extras}>
      {children}
    </a>
  ) : (
    <GatsbyLink to={href} {...extras}>
      {children}
    </GatsbyLink>
  );
};

export default Link;
