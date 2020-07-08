import navigationConfig from "../config/navigation.json";

interface ILink {
  title: string;
  path: string;
}

interface NavigationConfig {
  configKey: "navigation";
  links: ILink[];
}

const useNavigationConfig = () => {
  return navigationConfig as NavigationConfig;
};

export default useNavigationConfig;
