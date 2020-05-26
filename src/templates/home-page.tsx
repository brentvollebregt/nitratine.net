import React from "react";
import { graphql } from "gatsby";

import Base from "../components/Base";
import Header from "../components/Home/Header";
import FeaturedPosts from "../components/Home/FeaturedPosts";

interface IHomePageTemplate {
  image: string;
  leadText: string;
  buttons: {
    text: string;
    link: string;
    type: string;
  }[];
}

export const HomePageTemplate: React.FC<IHomePageTemplate> = ({ image, leadText, buttons }) => (
  <>
    <Header image={image} leadText={leadText} buttons={buttons} />
    <FeaturedPosts />
  </>
);

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
