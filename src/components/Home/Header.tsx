import React from "react";
import { Link } from "gatsby";
import { Button, Jumbotron } from "react-bootstrap";
import { isExternalPath } from "../utils";
import "./Header.scss";

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
  <Jumbotron fluid className="text-center header">
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
  </Jumbotron>
);

export default Header;
