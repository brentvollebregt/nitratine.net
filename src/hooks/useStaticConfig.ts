import staticConfig from "../config/static.json";

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
}

const useStaticConfig = () => {
  return staticConfig as StaticConfig;
};

export default useStaticConfig;
