import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import Home, { IHome } from "../components/Home";
import { FeaturedPostSummary } from "../components/Home/FeaturedPosts";

export const HomePageTemplate: React.FC<IHome> = props => <Home {...props} />;

const HomePage = ({ data }) => {
  const { frontmatter } = data.markdownRemark;

  const postSummaries: FeaturedPostSummary[] = data.posts.edges.map(({ node }) => ({
    slug: node.fields.slug,
    title: node.frontmatter.title,
    description: node.frontmatter.description,
    date: new Date(node.frontmatter.date),
    category: node.frontmatter.category,
    image: node.frontmatter.image.publicURL
  }));

  return (
    <Base>
      <HomePageTemplate
        image={frontmatter.image.childImageSharp.fluid.src}
        leadText={frontmatter.leadText}
        buttons={frontmatter.buttons}
        featuredPosts={frontmatter.featuredPosts}
        postSummaries={postSummaries}
      />
    </Base>
  );
};

export default HomePage;

export const pageQuery = graphql`
  query HomePage {
    markdownRemark(frontmatter: { templateKey: { eq: "home-page" } }) {
      frontmatter {
        image {
          childImageSharp {
            fluid(maxWidth: 2048, quality: 100) {
              ...GatsbyImageSharpFluid
            }
          }
        }
        leadText
        buttons {
          text
          link
          type
        }
        featuredPosts {
          type
          post
          rawHtml
          rawLink
        }
      }
    }
    posts: allMarkdownRemark(
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
            description
            date
            category
            image {
              publicURL
            }
          }
        }
      }
    }
  }
`;
