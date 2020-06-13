import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import Portfolio, { IPortfolio } from "../components/Portfolio";

export const PortfolioPageTemplate: React.FC<IPortfolio> = props => {
  return <Portfolio {...props} />;
};

const AboutPage = ({ data }) => {
  return (
    <Base>
      <PortfolioPageTemplate
        snippets={() => <div dangerouslySetInnerHTML={{ __html: data.markdownRemark.html }} />}
      />
    </Base>
  );
};

export default AboutPage;

export const aboutPageQuery = graphql`
  query PortfolioPage {
    markdownRemark(frontmatter: { templateKey: { eq: "portfolio-page" } }) {
      html
    }
  }
`;
