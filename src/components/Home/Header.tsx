import React from "react";
import { Button } from "react-bootstrap";
import "./Header.scss";
import { Link } from "gatsby";
import { isExternalPath } from "../utils";

export interface IHeader {
  image: string;
  leadText: string;
  buttons: {
    text: string;
    link: string;
    type: string;
  }[];
}

const Header: React.FC<IHeader> = ({ image, leadText, buttons }) => (
  <section className="jumbotron jumbotron-fluid text-center header">
    <h1 className="sr-only">Nitratine</h1>
    <img src={image} className="img-fluid mb-2" />
    <p className="lead text-muted">{leadText}</p>
    <p>
      {buttons.map(({ text, link, type }) => (
        <Button
          key={text}
          href={link}
          as={isExternalPath(link) ? undefined : Link}
          to={link} // to is for Link
          variant={type as any}
          className="my-2 mx-1"
        >
          {text}
        </Button>
      ))}
    </p>
  </section>
);

export default Header;
