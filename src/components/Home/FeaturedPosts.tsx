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
  rawLink: string;
}

type FeaturedPostType = PostFeaturedPostType | PostImageFeaturedPostType | RawFeaturedPostType;

export interface IFeaturedPosts {
  featuredPosts: FeaturedPostType[];
}

const FeaturedPosts: React.FC<IFeaturedPosts> = ({ featuredPosts }) => {
  const postSummaries = usePostSummaries();

  return (
    <div className="featured-posts">
      <div className="card-columns">
        {featuredPosts.map(p => (
          <FeaturedPost
            featuredPost={p}
            associatedPostSummary={postSummaries.find(s => s.slug === `/blog/post/${p.post}/`)}
          />
        ))}
      </div>
    </div>
  );
};

interface IFeaturedPost {
  featuredPost: FeaturedPostType;
  associatedPostSummary: PostSummary | undefined;
}

const FeaturedPost: React.FC<IFeaturedPost> = ({ featuredPost, associatedPostSummary }) => {
  switch (featuredPost.type) {
    case "post":
    case "postImage": {
      return (
        <a href={associatedPostSummary?.slug}>
          <div className="card card-hover-effect">
            <img className="card-img-top" src={associatedPostSummary?.image} alt="Post Thumbnail" />
            {featuredPost.type === "post" && (
              <div className="card-body">
                <h5 className="card-title">{associatedPostSummary?.title}</h5>
                <p className="card-text">{associatedPostSummary?.description}</p>
                <small className="text-muted">
                  {associatedPostSummary !== undefined
                    ? formatDate(associatedPostSummary.date)
                    : ""}
                </small>
                <span className="ml-2 badge badge-primary">{associatedPostSummary?.category}</span>
              </div>
            )}
          </div>
        </a>
      );
    }
    case "raw": {
      const link = featuredPost.rawLink ?? associatedPostSummary?.slug;
      return (
        <a href={link}>
          <div
            className="card card-hover-effect"
            dangerouslySetInnerHTML={{ __html: featuredPost.rawHtml }}
          />
        </a>
      );
    }
  }
};

export default FeaturedPosts;
