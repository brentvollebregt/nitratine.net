import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import Home, { IHome } from "../components/Home";

export const HomePageTemplate: React.FC<IHome> = props => <Home {...props} />;

const HomePage = ({ data }) => {
  const { frontmatter } = data.markdownRemark;

  return (
    <Base>
      <HomePageTemplate
        image={frontmatter.image.childImageSharp.fluid.src}
        leadText={frontmatter.leadText}
        buttons={frontmatter.buttons}
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
      }
    }
  }
`;
