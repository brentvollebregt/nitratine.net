import CMS from "netlify-cms-app";

import AboutPagePreview from "./preview-templates/AboutPagePreview";
import HomePagePreview from "./preview-templates/HomePagePreview";
import PostPreview from "./preview-templates/PostPreview";
import PortfolioPagePreview from "./preview-templates/PortfolioPagePreview";

CMS.registerPreviewTemplate("home", HomePagePreview);
CMS.registerPreviewTemplate("about", AboutPagePreview);
CMS.registerPreviewTemplate("post", PostPreview);
CMS.registerPreviewTemplate("portfolio", PortfolioPagePreview);
