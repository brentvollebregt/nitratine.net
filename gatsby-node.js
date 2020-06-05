const path = require("path");
const { createFilePath } = require("gatsby-source-filesystem");
const { fmImagesToRelative } = require("gatsby-remark-relative-images");

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

  // // Tag pages:
  // let tags = [];
  // // Iterate through each post, putting all found tags into `tags`
  // posts.forEach(edge => {
  //   if (_.get(edge, `node.frontmatter.tags`)) {
  //     tags = tags.concat(edge.node.frontmatter.tags);
  //   }
  // });
  // // Eliminate duplicate tags
  // tags = _.uniq(tags);

  // // Make tag pages
  // tags.forEach(tag => {
  //   const tagPath = `/tags/${_.kebabCase(tag)}/`;

  //   createPage({
  //     path: tagPath,
  //     component: path.resolve(`src/templates/tags.js`),
  //     context: {
  //       tag
  //     }
  //   });
  // });
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
