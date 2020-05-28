import { useStaticQuery, graphql } from "gatsby";

interface IUseSiteMetadata {
  title: string;
}

export const useSiteMetadata = (): IUseSiteMetadata => {
  const { site } = useStaticQuery(
    graphql`
      query SiteMetaData {
        site {
          siteMetadata {
            title
          }
        }
      }
    `
  );

  return site.siteMetadata;
};
