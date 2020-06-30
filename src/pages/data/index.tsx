import React from "react";
import { graphql } from "gatsby";
import Base from "../../components/Base";

const Data = ({ data }: { data: Query }) => {
  const postsSortedByDate = data.posts.edges.sort(
    (a, b) => -a.node.frontmatter.date.localeCompare(b.node.frontmatter.date)
  );
  const githubRepositoriesSortedByStars = data.githubRepositories.repositories.sort(
    (a, b) => b.stargazers_count - a.stargazers_count
  );

  return (
    <Base>
      <div className="row justify-content-center mb-5">
        <div className="col-xs-12 col-lg-8">
          <h1>Data</h1>
          <p>
            This page is a place where you can see view counts for all my pages, GitHub repo stats
            and other numbers related to the work I do.
          </p>

          <h2>Post View Counts</h2>
          <p>
            These counts are counted using{" "}
            <a href="https://hitcounter.pythonanywhere.com">hitcounter.pythonanywhere.com</a>. They
            are not 100% accurate but will be a reasonable idea of the actual views (better than
            Google Analytics being blocked by ad-blockers)
          </p>
          <table>
            <thead>
              <tr>
                <th>Post</th>
                <th>Hits</th>
              </tr>
            </thead>
            <tbody>
              {postsSortedByDate.map(({ node }) => (
                <tr>
                  <td>
                    <a href={node.fields.slug}>{node.frontmatter.title}</a>
                  </td>
                  <td>
                    <img
                      src={`https://hitcounter.pythonanywhere.com/nocount/tag.svg?url=https://nitratine.net${node.fields.slug}`}
                      alt={`Hits for ${node.frontmatter.title}`}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2>GitHub Repository Stats</h2>
          <table>
            <thead>
              <tr>
                <th>Repository</th>
                <th>Stars</th>
                <th>Forks</th>
                <th>Watchers</th>
              </tr>
            </thead>
            <tbody>
              {githubRepositoriesSortedByStars.map(({ full_name }) => (
                <tr>
                  <td>
                    <a href={`https://github.com/${full_name}`}>{full_name}</a>
                  </td>
                  <td>
                    <img
                      src={`https://img.shields.io/github/stars/${full_name}.svg?style=social`}
                      alt={`Stars for ${full_name}`}
                    />
                  </td>
                  <td>
                    <img
                      src={`https://img.shields.io/github/forks/${full_name}.svg?style=social`}
                      alt={`Forks for ${full_name}`}
                    />
                  </td>
                  <td>
                    <img
                      src={`https://img.shields.io/github/watchers/${full_name}.svg?style=social`}
                      alt={`Watchers for ${full_name}`}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2>Other</h2>
          <table>
            <thead>
              <tr>
                <th>Item</th>
                <th>Statistic</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <a href="https://www.youtube.com/PyTutorials">YouTube Subscribers</a>
                </td>
                <td>
                  {/* TODO */}
                  {/* <script src="https://apis.google.com/js/platform.js" gapi_processed="true"></script>
                                    <div class="g-ytsubscribe" data-channel="PrivateSplat" data-layout="default" data-count="default"></div> */}
                </td>
              </tr>
              <tr>
                <td>
                  <a href="https://github.com/brentvollebregt">GitHub Followers</a>
                </td>
                <td>
                  <img
                    src="https://img.shields.io/github/followers/brentvollebregt.svg?style=social"
                    alt="GitHub Followers"
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <a href="https://twitter.com/PyTutorials">Twitter Followers</a>
                </td>
                <td>
                  <img
                    src="https://img.shields.io/twitter/follow/pytutorials.svg?style=social"
                    alt="Twitter Followers"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Base>
  );
};

interface Query {
  posts: {
    edges: {
      node: {
        fields: {
          slug: string;
        };
        frontmatter: {
          title: string;
          date: string;
        };
      };
    }[];
  };
  githubRepositories: {
    repositories: {
      stargazers_count: number;
      full_name: string;
    }[];
  };
}

export const categoryPageQuery = graphql`
  {
    posts: allMarkdownRemark(filter: { frontmatter: { templateKey: { eq: "blog-post" } } }) {
      edges {
        node {
          fields {
            slug
          }
          frontmatter {
            title
            date
          }
        }
      }
    }
    githubRepositories {
      repositories {
        stargazers_count
        full_name
      }
    }
  }
`;

export default Data;
