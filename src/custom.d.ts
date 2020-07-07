declare module "*.svg" {
  const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  export default content;
}

declare module "gatsby-plugin-disqus" {
  const Disqus: React.FC<{
    config: {
      url: string;
      identifier: string;
      title: string;
    };
  }>;
}
