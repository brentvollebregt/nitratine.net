import React from "react";
import { formatDate } from "../utils";
import "./FeaturedPosts.scss";
import usePostSummaries, { PostSummary } from "../../hooks/usePostSummaries";

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
            <FeaturedPost
              key={`${p.post}-${p.type}`}
              featuredPost={p}
              associatedPostSummary={associatedPostSummary}
            />
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
        <a href={associatedPostSummary.slug}>
          <div className="card card-hover-effect">
            <img className="card-img-top" src={associatedPostSummary.image} alt="Post Thumbnail" />
            {featuredPost.type === "post" && (
              <div className="card-body">
                <h5 className="card-title">{associatedPostSummary.title}</h5>
                <p className="card-text">{associatedPostSummary.description}</p>
                <small className="text-muted">{formatDate(associatedPostSummary.date)}</small>
                <span className="ml-2 badge badge-primary">{associatedPostSummary.category}</span>
              </div>
            )}
          </div>
        </a>
      );
    }
    case "raw":
    case "rawBody": {
      return (
        <a href={associatedPostSummary.slug}>
          <div className="card card-hover-effect">
            {featuredPost.type === "rawBody" && (
              <img className="card-img-top" src={associatedPostSummary.image} alt="Thumbnail" />
            )}
            <div dangerouslySetInnerHTML={{ __html: featuredPost.rawHtml }} />
          </div>
        </a>
      );
    }
  }
};

export default FeaturedPosts;
