import React, { useEffect } from "react";
import Link from "../Helpers/Link";
import SEO from "../Helpers/SEO";
import YouTubeSubscribeButton from "../Helpers/YouTubeSubscribeButton";
import usePostSummaries from "../../hooks/usePostSummaries";
import useGitHubRepositories from "../../hooks/useGitHubRepositories";

interface IData {}

const Data: React.FC<IData> = ({}) => {
  const postSummaries = usePostSummaries();
  const gitHubRepositories = useGitHubRepositories();

  const postsSortedByDate = postSummaries.sort((a, b) => b.date.valueOf() - a.date.valueOf());
  const githubRepositoriesSortedByStars = gitHubRepositories.sort(
    (a, b) => b.stargazers_count - a.stargazers_count
  );

  // If the GAPI has loaded, call it to create the subscribe button
  useEffect(() => {
    if ((window as any).gapi) {
      (window as any).gapi.ytsubscribe.go();
    }
  }, []);

  return (
    <>
      <SEO
        title="Data"
        description="This is a summary of the hits on each page on this site and summary figures for my GitHub repositories."
      />

      <div className="row justify-content-center">
        <div className="col-xs-12 col-lg-8">
          <h1>Data</h1>
          <p>
            This page is a place where you can see view counts for all my pages, GitHub repo stats
            and other numbers related to the work I do.
          </p>

          <h2>Post View Counts</h2>
          <p>
            These counts are counted using{" "}
            <Link href="https://hitcounter.pythonanywhere.com">hitcounter.pythonanywhere.com</Link>.
            They are not 100% accurate but will be a reasonable idea of the actual views (better
            than Google Analytics being blocked by ad-blockers)
          </p>
          <table>
            <thead>
              <tr>
                <th>Post</th>
                <th>Hits</th>
              </tr>
            </thead>
            <tbody>
              {postsSortedByDate.map(({ slug, title }) => (
                <tr>
                  <td>
                    <Link href={slug}>{title}</Link>
                  </td>
                  <td>
                    <img
                      src={`https://hitcounter.pythonanywhere.com/nocount/tag.svg?url=https://nitratine.net${slug}`}
                      alt={`Hits for ${title}`}
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
                    <Link href={`https://github.com/${full_name}`}>{full_name}</Link>
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
                  <Link href="https://www.youtube.com/PyTutorials">YouTube Subscribers</Link>
                </td>
                <td>
                  <YouTubeSubscribeButton layout="default" />
                </td>
              </tr>
              <tr>
                <td>
                  <Link href="https://github.com/brentvollebregt">GitHub Followers</Link>
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
                  <Link href="https://twitter.com/PyTutorials">Twitter Followers</Link>
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
    </>
  );
};

export default Data;
