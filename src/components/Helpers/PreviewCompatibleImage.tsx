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
  style?: React.CSSProperties;
}

const PreviewCompatibleImage: React.FC<IPreviewCompatibleImage> = ({
  childImageSharp,
  blob,
  alt,
  className,
  style
}) => {
  if (childImageSharp !== undefined) {
    return <Img fluid={childImageSharp.fluid} alt={alt} className={className} style={style} />;
  }

  if (blob !== undefined) {
    return <img src={blob} alt={alt} className={className} style={style} />;
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
