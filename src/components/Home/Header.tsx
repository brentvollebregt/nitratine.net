import React from "react";
import { Button } from "react-bootstrap";

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
  <section className="jumbotron jumbotron-fluid text-center" style={{ background: "transparent" }}>
    <h1 className="sr-only">Nitratine</h1>
    <img src={image} className="img-fluid mb-2" style={{ maxHeight: 150 }} />
    <p className="lead text-muted">{leadText}</p>
    <p>
      {buttons.map(({ text, link, type }) => (
        <Button href={link} variant={type as any} className="my-2 mx-1" key={text}>
          {text}
        </Button>
      ))}
    </p>
  </section>
);

export default Header;
