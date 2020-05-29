import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import About, { IAbout, IAboutExperience } from "../components/About";

export const AboutPageTemplate: React.FC<IAbout> = ({ email, experience, body }) => {
  return <About body={body} experience={experience} email={email} />;
};

const AboutPage = ({ data }) => {
  const email: string = data.markdownRemark.frontmatter.email;
  const experience: IAboutExperience[] = data.markdownRemark.frontmatter.experience.map(e => ({
    title: e.title,
    img: e.img.publicURL
  }));
  const body = () => <div dangerouslySetInnerHTML={{ __html: data.markdownRemark.html }} />;

  return (
    <Base>
      <AboutPageTemplate email={email} experience={experience} body={body} />
    </Base>
  );
};

export default AboutPage;

export const aboutPageQuery = graphql`
  query AboutPage {
    markdownRemark(frontmatter: { templateKey: { eq: "about-page" } }) {
      html
      frontmatter {
        experience {
          title
          img {
            publicURL
          }
        }
        email
      }
    }
  }
`;
