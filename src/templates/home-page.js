import React from "react";
import PropTypes from "prop-types";
import { graphql } from "gatsby";
import { Button } from "react-bootstrap";

import Base from "../components/Base";
import Header from "../components/Home/Header";
import FeaturedPosts from "../components/Home/FeaturedPosts";

export const IndexPageTemplate = ({ image, leadText, buttons }) => (
  <>
    <Header image={image} leadText={leadText} buttons={buttons} />
    <FeaturedPosts />
  </>
);

IndexPageTemplate.propTypes = {
  image: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
  leadText: PropTypes.string,
  buttons: PropTypes.object
};

const IndexPage = ({ data }) => {
  const { frontmatter } = data.markdownRemark;

  return (
    <Base>
      <IndexPageTemplate
        image={frontmatter.image}
        leadText={frontmatter.leadText}
        buttons={frontmatter.buttons}
      />
    </Base>
  );
};

IndexPage.propTypes = {
  data: PropTypes.shape({
    markdownRemark: PropTypes.shape({
      frontmatter: PropTypes.object
    })
  })
};

export default IndexPage;

export const pageQuery = graphql`
  query IndexPageTemplate {
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
