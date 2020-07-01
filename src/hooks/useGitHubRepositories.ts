import { useStaticQuery, graphql } from "gatsby";

export interface GitHubRepositorySummary {
  // There are move fields than these in the API that have not been added
  stargazers_count: number;
  full_name: string;
}

const useGitHubRepositories = (): GitHubRepositorySummary[] => {
  const { githubRepositories } = useStaticQuery(graphql`
    query GitHubRepositories {
      githubRepositories {
        repositories {
          stargazers_count
          full_name
        }
      }
    }
  `);

  return githubRepositories.repositories;
};

export default useGitHubRepositories;
