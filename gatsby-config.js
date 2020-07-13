const staticConfig = require("./src/config/static.json");

module.exports = {
  siteMetadata: {
    siteUrl: staticConfig.siteUrl,
    title: staticConfig.title,
    description: staticConfig.description,
    blogFeed: {
      postsPerPage: staticConfig.blogFeed.postsPerPage,
      pagesEitherSideOfCurrentInPagination:
        staticConfig.blogFeed.pagesEitherSideOfCurrentInPagination
    }
  },
  plugins: [
    "gatsby-plugin-react-helmet",
    {
      // Google Analytics
      resolve: `gatsby-plugin-google-analytics`,
      options: {
        trackingId: staticConfig.googleAnalyticsId,
        head: true
      }
    },
    "gatsby-plugin-sass",
    {
      // Static assets
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/static/assets`,
        name: "uploads"
      }
    },
    {
      // Site pages
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/src/pages`,
        name: "pages"
      }
    },
    "gatsby-plugin-sharp",
    "gatsby-transformer-sharp",
    {
      // Markdown transformer
      resolve: "gatsby-transformer-remark",
      options: {
        tableOfContents: {
          heading: null,
          maxDepth: 3
        },
        plugins: [
          {
            // Putting links on headers
            resolve: "gatsby-remark-autolink-headers",
            options: {
              offsetY: "60" // Header height (56) + a little more (4)
            }
          },
          {
            // Convert image src(s) in markdown to be relative to their node's parent directory.
            resolve: "gatsby-remark-relative-images",
            options: {
              name: "uploads"
            }
          },
          {
            // Resizing images in markdown + blur up
            resolve: "gatsby-remark-images",
            options: {
              maxWidth: 2048,
              quality: 90
            }
          },
          {
            // Copies local files linked to/from Markdown (.md|.markdown) files to the root directory
            resolve: "gatsby-remark-copy-linked-files",
            options: {
              destinationDir: "static",
              ignoreFileExtensions: []
            }
          },
          {
            // Syntax highlighting
            resolve: `gatsby-remark-prismjs`,
            options: {
              showLineNumbers: false
            }
          }
        ]
      }
    },
    {
      resolve: `gatsby-plugin-disqus`,
      options: {
        shortname: `nitratine`
      }
    },
    "gatsby-plugin-typescript",
    {
      // Sitemap
      resolve: `gatsby-plugin-sitemap`,
      options: {
        query: `{
          site {
            siteMetadata {
              siteUrl
            }
          }
          allFile(filter: {extension: {eq: "md"}}) {
            edges {
              node {
                modifiedTime
                relativePath
              }
            }
          }
          allSitePage {
            nodes {
              path
            }
          }
        }`,
        serialize: ({ site, allFile, allSitePage }) =>
          allSitePage.nodes.map(node => {
            const filePresent = allFile.edges.find(
              item =>
                `/${item.node.relativePath.replace("index.md", "").replace(".md", "")}` ===
                node.path
            );
            return {
              url: `${site.siteMetadata.siteUrl}${node.path}`,
              lastmod: filePresent
                ? filePresent.node.modifiedTime.split("T")[0]
                : new Date().toISOString().split("T")[0]
            };
          })
      }
    },
    {
      // Automatically shows the nprogress indicator when a page is delayed in loading
      resolve: `gatsby-plugin-nprogress`,
      options: {
        color: `#cf1664`,
        showSpinner: false
      }
    },
    {
      // Favicon, manifest and other common header stuff
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `Nitratine`,
        short_name: `Nitratine`,
        start_url: `/`,
        background_color: `#ffffff`,
        theme_color: `#343a40`,
        display: `standalone`,
        icon: `static/assets/favicon.png`
      }
    },
    {
      // RSS Feed
      resolve: `gatsby-plugin-feed`,
      options: {
        query: ` 
          {
            site {
              siteMetadata {
                title
                description
                siteUrl
                site_url: siteUrl
              }
            }
          }
        `,
        feeds: [
          {
            output: "/rss.xml",
            title: "Nitratine",
            match: "^/blog/", // TODO Maybe remove
            serialize: ({ query: { site, allMarkdownRemark } }) => {
              return allMarkdownRemark.edges.map(edge => {
                const { title, date, description, tags, image } = edge.node.frontmatter;
                const { slug } = edge.node.fields;
                const { html } = edge.node;
                return Object.assign({}, edge.node.frontmatter, {
                  title: title,
                  date: date,
                  description: description,
                  categories: tags,
                  url: site.siteMetadata.siteUrl + slug,
                  guid: site.siteMetadata.siteUrl + slug,
                  custom_elements: [{ "content:encoded": html }],
                  enclosure: { url: image.childImageSharp.fixed.src }
                });
              });
            },
            query: `
              {
                allMarkdownRemark(
                  filter: { frontmatter: { templateKey: { eq: "blog-post" }, hidden: { eq: false } } }
                  sort: { order: DESC, fields: [frontmatter___date] },
                ) {
                  edges {
                    node {
                      html
                      fields {
                        slug
                      }
                      frontmatter {
                        title
                        date
                        description
                        tags
                        image {
                          childImageSharp {
                            fixed {
                              src
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            `
          }
        ]
      }
    },
    {
      // Netlify CMS
      resolve: "gatsby-plugin-netlify-cms",
      options: {
        modulePath: `${__dirname}/src/cms/cms.tsx`
      }
    }
    // {
    //   resolve: "gatsby-plugin-purgecss", // purges all unused/unreferenced css rules
    //   options: {
    //     develop: true, // Activates purging in npm run develop
    //     // purgeOnly: ["/all.scss"],
    //     whitelist: ["btn-primary"]
    //   }
    // } // must be after other CSS plugins
  ]
};
