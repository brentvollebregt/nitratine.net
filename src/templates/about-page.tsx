import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";

interface IAboutPageTemplate {
  email: string;
  experience: {
    title: string;
    img: string;
  }[];
  body: React.FC;
}

export const AboutPageTemplate: React.FC<IAboutPageTemplate> = ({ email, experience, body }) => {
  const AboutBody = body;
  return (
    <div>
      <h1>About Me</h1>
      <AboutBody />

      <h2>Tech I Have Had Experience With</h2>
      <div className="tech-icon-container mb-3">
        {experience.map(({ title, img }) => (
          <img src={img} title={title} alt={title} key={title} />
        ))}
      </div>

      <h2 id="donations">Donations</h2>
      <p>If you would like to donate for any project I maintain, this is the place to do so.</p>
      <form
        action="https://www.paypal.com/cgi-bin/webscr"
        method="post"
        target="_top"
        className="mb-3"
      >
        <input type="hidden" name="cmd" value="_s-xclick" />
        <input type="hidden" name="hosted_button_id" value="CG8P7ELK4RG26" />
        <input
          type="image"
          src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"
          name="submit"
          alt="PayPal - The safer, easier way to pay online!"
        />
        <img
          alt=""
          src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif"
          width="1"
          height="1"
        />
      </form>

      <h2 id="contact">Contact</h2>
      <p>
        If you have any questions about a YouTube video, please leave the question in the comments
        and for questions about a blog post, leave the question in the comments on the blog post.
        Emails regarding this nature will be referred back to the corresponding platform.
      </p>
      <p>If you would like to contact me for another reason, send an email to {email}.</p>
    </div>
  );
};

const AboutPage = ({ data }) => {
  const { email } = data.markdownRemark.frontmatter;
  const experience = data.markdownRemark.frontmatter.experience.map(e => ({
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
