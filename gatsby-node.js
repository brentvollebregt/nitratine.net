const path = require("path");
const axios = require("axios").default;
const { createFilePath } = require("gatsby-source-filesystem");
const { fmImagesToRelative } = require("gatsby-remark-relative-images");
require("dotenv").config({ path: `.env` });

exports.sourceNodes = async ({ actions: { createNode }, createNodeId, createContentDigest }) => {
  const youTubeDataApiKey = process.env.YOUTUBE_DATA_API_KEY;
  if (youTubeDataApiKey === "") {
    throw Error("YOUTUBE_DATA_API_KEY has not been set");
  }

  const channelId = "UCesEknt3SRX9R9W_f93Tb7g"; // TODO Pull out into sidebar settings
  const maxResults = 6;
  const { data } = await axios.get(
    `https://www.googleapis.com/youtube/v3/search?key=${youTubeDataApiKey}&channelId=${channelId}&part=snippet&order=date&maxResults=${maxResults}&type=video`
  );

  createNode({
    ...data,
    parent: null,
    children: [],
    id: createNodeId(`recent-youtube-videos`),
    internal: {
      type: `RecentYouTubeVideo`,
      contentDigest: createContentDigest(data)
    }
  });
};

exports.createPages = async ({ actions, graphql, reporter }) => {
  const { createPage } = actions;

  // Get all posts to create post-related pages
  const { errors: postErrors, data: postData } = await graphql(`
    {
      site {
        siteMetadata {
          blogFeed {
            postsPerPage
          }
        }
      }

      posts: allMarkdownRemark(
        filter: { frontmatter: { templateKey: { eq: "blog-post" } } }
        sort: { fields: [frontmatter___date], order: ASC }
      ) {
        edges {
          node {
            id
            fields {
              slug
            }
            frontmatter {
              tags
              templateKey
            }
          }
          next {
            id
          }
          previous {
            id
          }
        }
      }
    }
  `);

  if (postErrors) {
    reporter.panicOnBuild(`Error while running GraphQL query.`);
    postErrors.forEach(e => console.error(e.toString()));
    return;
  }

  // Data from the query
  const postsPerPage = postData.site.siteMetadata.blogFeed.postsPerPage;
  const posts = postData.posts.edges;

  // Create blog-feed-page pages
  const numPages = Math.ceil(posts.length / postsPerPage);
  Array.from({ length: numPages }).forEach((_, i) => {
    createPage({
      path: i === 0 ? `/blog` : `/blog/page/${i + 1}`,
      component: path.resolve("src/templates/blog-feed-page.tsx"),
      context: {
        limit: postsPerPage,
        skip: i * postsPerPage,
        numPages,
        currentPage: i + 1
      }
    });
  });

  // Create blog pages
  posts.forEach(edge => {
    const id = edge.node.id;
    const nextPostId = edge.next === null ? null : edge.next.id;
    const previousPostId = edge.previous === null ? null : edge.previous.id;
    createPage({
      path: edge.node.fields.slug,
      tags: edge.node.frontmatter.tags,
      component: path.resolve(`src/templates/${String(edge.node.frontmatter.templateKey)}.tsx`),
      context: {
        id,
        nextPostId,
        previousPostId
      }
    });
  });

  // Get all non-post pages
  const { errors: pageErrors, data: pageData } = await graphql(`
    {
      allMarkdownRemark(filter: { frontmatter: { templateKey: { ne: "blog-post" } } }) {
        edges {
          node {
            id
            fields {
              slug
            }
            frontmatter {
              templateKey
            }
          }
        }
      }
    }
  `);

  if (pageErrors) {
    reporter.panicOnBuild(`Error while running GraphQL query.`);
    pageErrors.forEach(e => console.error(e.toString()));
    return;
  }

  const pages = pageData.allMarkdownRemark.edges;

  // Create each non-post page
  pages.forEach(edge => {
    const id = edge.node.id;
    createPage({
      path: edge.node.fields.slug,
      component: path.resolve(`src/templates/${String(edge.node.frontmatter.templateKey)}.tsx`),
      context: {
        id
      }
    });
  });
};

exports.onCreateNode = ({ node, actions, getNode }) => {
  const { createNodeField } = actions;
  fmImagesToRelative(node); // convert image paths for gatsby images

  if (node.internal.type === `MarkdownRemark`) {
    const value = createFilePath({ node, getNode });
    createNodeField({
      name: `slug`,
      node,
      value
    });
  }
};
