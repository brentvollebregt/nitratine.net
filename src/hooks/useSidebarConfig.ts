import sidebarConfig from "../config/sidebar.json";

interface ICategoryPrefix {
  category: string;
  prefix: string;
}

interface IFeaturedSites {
  title: string;
  imageSrc: string;
  href: string;
}

interface SidebarConfig {
  configKey: "sidebar";
  about: string;
  categoryPrefixes: ICategoryPrefix[];
  featuredSites: IFeaturedSites[];
}

const useSidebarConfig = () => {
  return sidebarConfig as SidebarConfig;
};

export default useSidebarConfig;
