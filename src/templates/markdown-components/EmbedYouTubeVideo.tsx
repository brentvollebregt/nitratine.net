import React from "react";
import "./EmbedYouTubeVideo.scss";

interface IEmbedYouTubeVideo {
  id: string;
}

const EmbedYouTubeVideo: React.FC<IEmbedYouTubeVideo> = ({ id }) => {
  return (
    <div className="embedded_yt my-3">
      <div>
        <iframe
          allow="autoplay; encrypted-media"
          allowFullScreen={true}
          src={`https://www.youtube.com/embed/${id}`}
        />
      </div>
    </div>
  );
};

export default EmbedYouTubeVideo;
