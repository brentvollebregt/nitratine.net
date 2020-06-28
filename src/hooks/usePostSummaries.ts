import { useStaticQuery, graphql } from "gatsby";
import { IPreviewCompatibleImageSource } from "../components/Helpers/PreviewCompatibleImage";

export interface PostSummary {
  slug: string;
  title: string;
  date: Date;
  category: string;
  tags: string[];
  hidden: boolean;
  githubRepository: string | null;
  description: string;
  image: IPreviewCompatibleImageSource | undefined;
}

const usePostSummaries = (): PostSummary[] => {
  const { allMarkdownRemark } = useStaticQuery(graphql`
    query PostSummaries {
      allMarkdownRemark(
        filter: { frontmatter: { templateKey: { eq: "blog-post" } } }
        sort: { fields: [frontmatter___date], order: ASC }
      ) {
        edges {
          node {
            fields {
              slug
            }
            frontmatter {
              title
              date
              category
              tags
              hidden
              githubRepository
              description
              image {
                childImageSharp {
                  fluid(maxWidth: 2048, quality: 100) {
                    ...GatsbyImageSharpFluid
                  }
                }
              }
            }
          }
        }
      }
    }
  `);

  const postSummaries: PostSummary[] = allMarkdownRemark.edges.map(({ node }: any) => ({
    slug: node.fields.slug,
    title: node.frontmatter.title,
    date: new Date(node.frontmatter.date),
    category: node.frontmatter.category,
    tags: node.frontmatter.tags,
    hidden: node.frontmatter.hidden,
    githubRepository: node.frontmatter.githubRepository,
    description: node.frontmatter.description,
    image: node.frontmatter.image
  }));

  return postSummaries;
};

export default usePostSummaries;
