import { useStaticQuery, graphql } from "gatsby";

interface IUseSiteMetadata {
  title: string;
  blogFeed: {
    postsPerPage: number;
    pagesEitherSideOfCurrentInPagination: number;
  };
}

export const useSiteMetadata = (): IUseSiteMetadata => {
  const { site } = useStaticQuery(
    graphql`
      query SiteMetaData {
        site {
          siteMetadata {
            title
            blogFeed {
              postsPerPage
              pagesEitherSideOfCurrentInPagination
            }
          }
        }
      }
    `
  );

  return site.siteMetadata;
};
