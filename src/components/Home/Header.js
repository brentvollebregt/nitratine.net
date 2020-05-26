import React from "react";
import PropTypes from "prop-types";
import { Button } from "react-bootstrap";

const Header = ({ image, leadText, buttons }) => (
  <section class="jumbotron jumbotron-fluid text-center header">
    <h1 class="sr-only">Nitratine</h1>
    <img src={image.childImageSharp.fluid.src} class="img-fluid mb-2" />
    <p class="lead text-muted">{leadText}</p>
    <p>
      {buttons.map(({ text, link, type }) => (
        <Button href={link} variant={type} className="my-2 mx-1">
          {text}
        </Button>
      ))}
    </p>
  </section>
);

Header.propTypes = {
  image: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
  leadText: PropTypes.string,
  buttons: PropTypes.object
};

export default Header;
