import React from "react";
import "./EmbedYouTubeVideo.scss";

interface IEmbedYouTubeVideo {
  videoId: string;
}

const EmbedYouTubeVideo: React.FC<IEmbedYouTubeVideo> = ({ videoId }) => {
  return (
    <div className="embedded_yt my-3">
      <div>
        <iframe
          allow="autoplay; encrypted-media"
          allowFullScreen={true}
          src={`https://www.youtube.com/embed/${videoId}`}
        />
      </div>
    </div>
  );
};

export default EmbedYouTubeVideo;
