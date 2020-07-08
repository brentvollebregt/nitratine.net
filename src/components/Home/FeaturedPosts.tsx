import React from "react";
import { Card, Badge } from "react-bootstrap";
import Link from "../Helpers/Link";
import PreviewCompatibleImage from "../Helpers/PreviewCompatibleImage";
import usePostSummaries, { PostSummary } from "../../hooks/usePostSummaries";
import { formatDate } from "../utils";
import "./FeaturedPosts.scss";

interface PostFeaturedPostType {
  type: "post";
  post: string | null;
}

interface PostImageFeaturedPostType {
  type: "postImage";
  post: string | null;
}

interface RawFeaturedPostType {
  type: "raw";
  post: string | null;
  rawHtml: string;
}

interface RawBodyFeaturedPostType {
  type: "rawBody";
  post: string | null;
  rawHtml: string;
}

type FeaturedPostType =
  | PostFeaturedPostType
  | PostImageFeaturedPostType
  | RawFeaturedPostType
  | RawBodyFeaturedPostType;

export interface IFeaturedPosts {
  featuredPosts: FeaturedPostType[];
}

const FeaturedPosts: React.FC<IFeaturedPosts> = ({ featuredPosts }) => {
  const postSummaries = usePostSummaries();

  return (
    <div className="featured-posts">
      <div className="card-columns">
        {featuredPosts.map(p => {
          const associatedPostSummary = postSummaries.find(s => s.slug === `/blog/post/${p.post}/`);
          if (associatedPostSummary === undefined) {
            throw new Error(`Unable to find post with slug ${p.post}`);
          }

          return (
            <Link href={associatedPostSummary.slug} key={associatedPostSummary.slug}>
              <FeaturedPost
                key={`${p.post}-${p.type}`}
                featuredPost={p}
                associatedPostSummary={associatedPostSummary}
              />
            </Link>
          );
        })}
      </div>
    </div>
  );
};

interface IFeaturedPost {
  featuredPost: FeaturedPostType;
  associatedPostSummary: PostSummary;
}

const FeaturedPost: React.FC<IFeaturedPost> = ({ featuredPost, associatedPostSummary }) => {
  switch (featuredPost.type) {
    case "post":
    case "postImage": {
      return (
        <Card className="card-hover-effect">
          {associatedPostSummary.image !== undefined && (
            <PreviewCompatibleImage
              childImageSharp={associatedPostSummary.image.childImageSharp}
              alt="Post Thumbnail"
              className="card-img-top"
            />
          )}
          {featuredPost.type === "post" && (
            <Card.Body>
              <Card.Title>{associatedPostSummary.title}</Card.Title>
              <Card.Text>{associatedPostSummary.description}</Card.Text>
              <small className="text-muted">{formatDate(associatedPostSummary.date)}</small>
              <Badge variant="primary" className="ml-2">
                {associatedPostSummary.category}
              </Badge>
            </Card.Body>
          )}
        </Card>
      );
    }
    case "raw":
    case "rawBody": {
      return (
        <Card className="card-hover-effect">
          {featuredPost.type === "rawBody" && associatedPostSummary.image !== undefined && (
            <PreviewCompatibleImage
              childImageSharp={associatedPostSummary.image.childImageSharp}
              alt="Post Thumbnail"
              className="card-img-top"
            />
          )}
          <div dangerouslySetInnerHTML={{ __html: featuredPost.rawHtml }} />
        </Card>
      );
    }
  }
};

export default FeaturedPosts;
