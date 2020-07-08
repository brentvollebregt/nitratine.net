import staticConfig from "../config/static.json";

export type UseInternalLinkingOptions = "always" | "non-post-associations" | "never";

interface StaticConfig {
  configKey: "static";
  title: string;
  siteUrl: string;
  siteImage: string;
  blogFeed: {
    postsPerPage: number;
    pagesEitherSideOfCurrentInPagination: number;
  };
  social: {
    github: string;
    twitter: string;
  };
  adsense: {
    enabled: boolean;
    publisherId: string;
  };
  youtube: {
    channelId: string;
    recentViewAmount: number;
  };
  googleAnalyticsId: string;
  useInternalLinking: UseInternalLinkingOptions;
}

const useStaticConfig = () => {
  return staticConfig as StaticConfig;
};

export default useStaticConfig;
