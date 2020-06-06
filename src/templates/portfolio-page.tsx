import React from "react";
import { graphql } from "gatsby";
import ReactMarkdown from "react-markdown";
import Base from "../components/Base";
import Portfolio, { IPortfolio } from "../components/Portfolio";

export const PortfolioPageTemplate: React.FC<IPortfolio> = props => {
  return <Portfolio {...props} />;
};

const AboutPage = ({ data }) => {
  const snippets: React.FC[] = data.markdownRemark.frontmatter.snippets.map(s => () => (
    <ReactMarkdown source={s.body} />
  ));

  return (
    <Base>
      <PortfolioPageTemplate snippets={snippets} />
    </Base>
  );
};

export default AboutPage;

export const aboutPageQuery = graphql`
  query PortfolioPage {
    markdownRemark(frontmatter: { templateKey: { eq: "portfolio-page" } }) {
      frontmatter {
        snippets {
          body
        }
      }
    }
  }
`;
