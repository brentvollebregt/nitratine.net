import { useStaticQuery, graphql } from "gatsby";

export interface PostSummary {
  slug: string;
  title: string;
  date: Date;
  category: string;
  tags: string[];
  hidden: boolean;
  githubRepository: string | null;
  description: string;
  image: string;
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
                publicURL
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
    image: node.frontmatter.image.publicURL
  }));

  return postSummaries;
};

export default usePostSummaries;
