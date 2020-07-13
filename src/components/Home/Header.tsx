import React from "react";
import { Button, Jumbotron } from "react-bootstrap";
import Link from "../Helpers/Link";
import PreviewCompatibleImage, {
  IPreviewCompatibleImageSource
} from "../Helpers/PreviewCompatibleImage";
import "./Header.scss";
import useStaticConfig from "../../hooks/useStaticConfig";

export interface IHeader {
  image: IPreviewCompatibleImageSource;
  buttons: {
    text: string;
    link: string;
    type: string;
  }[];
}

const Header: React.FC<IHeader> = ({ image, buttons }) => {
  const { description } = useStaticConfig();

  return (
    <Jumbotron fluid className="text-center header">
      <h1 className="sr-only">Nitratine</h1>
      <div className="feature-image-wrapper mb-2">
        <PreviewCompatibleImage
          childImageSharp={image.childImageSharp}
          blob={image.blob}
          alt="Nitratine Logo"
        />
      </div>
      <p className="lead text-muted">{description}</p>
      <p>
        {buttons.map(({ text, link, type }) => (
          <Button key={text} href={link} as={Link} variant={type as any} className="my-2 mx-1">
            {text}
          </Button>
        ))}
      </p>
    </Jumbotron>
  );
};

export default Header;
