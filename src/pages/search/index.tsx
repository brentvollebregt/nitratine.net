import React from "react";
import Search from "../../components/Search";
import Base from "../../components/Base";
import BlogBase from "../../components/Blog/Base";

const SearchPage: React.FC = () => {
  return (
    <Base>
      <BlogBase>
        <Search />
      </BlogBase>
    </Base>
  );
};

export default SearchPage;
