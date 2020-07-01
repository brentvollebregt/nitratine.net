import React, { useState } from "react";
import SEO from "../Helpers/SEO";
import "./About.scss";

export interface IAboutExperience {
  title: string;
  img: string;
}

export interface IAbout {
  body: React.FC;
  experience: IAboutExperience[];
  email: string;
}

const About: React.FC<IAbout> = ({ body, experience, email }) => {
  const [emailDisplayed, setEmailDisplayed] = useState(false);

  const displayEmailAddress = (event: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => {
    // Stop the redirect - we need this because the a tag node will techincally be the same and
    // React will just swap out the contents. When this onClick completes, the browser will then
    // go to the href unless we stop it.
    event.preventDefault();

    // Show the alert
    alert(
      "Please leave questions about videos on YouTube and blog posts in the comments at the bottom of the post."
    );
    setEmailDisplayed(true);
  };

  const Body = body;
  return (
    <>
      <SEO
        title="About"
        description="My name is Brent and I'm a full-time software developer from New Zealand. My preferred language is Python but I also do a lot of development in frontend in my free time and use an assortment of other tech at work."
        relativePath="/about/"
      />

      <div className="about row justify-content-center mb-5">
        <div className="col-xs-12 col-lg-8">
          <Body />

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
            If you have any questions about a YouTube video, please leave the question in the
            comments and for questions about a blog post, leave the question in the comments on the
            blog post. Emails regarding this nature will be referred back to the corresponding
            platform.
          </p>
          <p>
            If you would like to contact me for another reason, send an email to{" "}
            {!emailDisplayed ? (
              <a href="#" onClick={displayEmailAddress}>
                [Display Email Address]
              </a>
            ) : (
              <a href={`mailto:${email}`}>{email}</a>
            )}
            .
          </p>
        </div>
      </div>
    </>
  );
};

export default About;
