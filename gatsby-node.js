const path = require("path");
const { writeFile, ensureDir, pathExists } = require("fs-extra");
const axios = require("axios").default;
const { createFilePath } = require("gatsby-source-filesystem");
const { fmImagesToRelative } = require("gatsby-remark-relative-images");
require("dotenv").config({ path: `.env` });

const staticConfig = require("./src/config/static.json");
const redirectsConfig = require("./src/config/redirects.json");
const siteBarConfig = require("./src/config/sidebar.json");

exports.sourceNodes = async ({ actions: { createNode }, createNodeId, createContentDigest }) => {
  // Get recent YouTube videos
  const youTubeDataApiKey = process.env.YOUTUBE_DATA_API_KEY;
  if (!youTubeDataApiKey) {
    throw Error(`YOUTUBE_DATA_API_KEY has not been set. Found "${youTubeDataApiKey}".`);
  }

  const { channelId, recentViewAmount } = siteBarConfig.youtube;
  const { data: youtubeData } = await axios.get(
    `https://www.googleapis.com/youtube/v3/search?key=${youTubeDataApiKey}&channelId=${channelId}&part=snippet&order=date&maxResults=${recentViewAmount}&type=video`
  );

  createNode({
    ...youtubeData,
    parent: null,
    children: [],
    id: createNodeId(`recent-youtube-videos`),
    internal: {
      type: `RecentYouTubeVideo`,
      contentDigest: createContentDigest(youtubeData)
    }
  });

  // Get GitHub repos
  const githubUsername = "brentvollebregt";
  if (!githubUsername) {
    throw Error(`GitHub username has not been set. Found "${githubUsername}".`);
  }

  const { data: githubData } = await axios.get(
    `https://api.github.com/users/${githubUsername}/repos`
  );
  const githubDataInObject = { repositories: githubData };

  createNode({
    ...githubDataInObject,
    parent: null,
    children: [],
    id: createNodeId(`github-repositories`),
    internal: {
      type: `GithubRepositories`,
      contentDigest: createContentDigest(githubDataInObject)
    }
  });
};

exports.createPages = async ({ actions, graphql, reporter }) => {
  const { createPage, createRedirect } = actions;

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

  // Create redirects
  redirectsConfig.redirects.forEach(({ from, to }) => {
    createRedirect({
      fromPath: from,
      isPermanent: true,
      redirectInBrowser: true,
      toPath: to
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

exports.onPostBuild = async ({ store }) => {
  const { redirects, program, config } = store.getState();

  let pathPrefix = program.prefixPaths ? config.pathPrefix : "";
  const folder = path.join(program.directory, "public");

  if (redirects.length !== undefined) {
    for (const redirect of redirects) {
      const { fromPath, toPath } = redirect;

      const FILE_PATH = path.join(folder, fromPath.replace(pathPrefix, ""), "index.html");

      const fileExists = await pathExists(FILE_PATH);
      if (!fileExists) {
        try {
          await ensureDir(path.dirname(FILE_PATH));
        } catch (err) {
          // ignore if the directory already exists;
        }

        const redirectToAbsolutePath = staticConfig.siteUrl + toPath;
        const redirectHtmlLines = [
          "<!DOCTYPE HTML>",
          '<html lang="en-US">',
          "\t<head>",
          "\t\t<title>Page Redirection</title>",
          '\t\t<meta charset="UTF-8">',
          `\t\t<meta http-equiv="refresh" content="0; url=${redirectToAbsolutePath}">`,
          '\t\t<script type="text/javascript">',
          `\t\t\twindow.location.href = "${redirectToAbsolutePath}"`,
          "\t\t</script>",
          "\t</head>",
          "\t<body>",
          `\t\tThis page has been moved. If you are not redirected automatically, follow this <a href='${redirectToAbsolutePath}'>link</a>.`,
          "\t</body>",
          "</html>"
        ];
        const redirectHtml = redirectHtmlLines.join("\n");
        await writeFile(FILE_PATH, redirectHtml);
      }
    }
  }
};
