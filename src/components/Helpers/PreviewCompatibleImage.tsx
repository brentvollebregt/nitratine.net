import React from "react";
import Img, { FluidObject } from "gatsby-image";

export interface IPreviewCompatibleImageSource {
  childImageSharp?: {
    fluid: FluidObject;
  };
  blob?: string;
}

export interface IPreviewCompatibleImage extends IPreviewCompatibleImageSource {
  alt?: string;
  className?: string;
}

const PreviewCompatibleImage: React.FC<IPreviewCompatibleImage> = ({
  childImageSharp,
  blob,
  alt,
  className
}) => {
  if (childImageSharp !== undefined) {
    return <Img fluid={childImageSharp.fluid} alt={alt} className={className} />;
  }

  if (blob !== undefined) {
    return <img src={blob} alt={alt} className={className} />;
  }

  console.warn({
    childImageSharp,
    blob,
    alt,
    className
  });
  return <div>Unable to render image</div>;
};

export default PreviewCompatibleImage;
