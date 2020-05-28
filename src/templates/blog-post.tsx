import React from "react";
import { graphql } from "gatsby";
import Base from "../components/Base";
import BlogBase from "../components/Blog/BlogBase";

interface IBlogPostTemplate {
  title: string;
  date: Date;
  category: string;
  tags: string[];
  hidden: boolean;
  githubRepository: string | null;
  description: string;
  body: React.FC;
}

export const BlogPostTemplate: React.FC<IBlogPostTemplate> = ({
  title,
  date,
  category,
  tags,
  hidden,
  githubRepository,
  description,
  body
}) => {
  const Body = body;
  return (
    // TODO Break this into more pieces into components/Blog/Post. Only show the top here, no pagination or comments
    <div className="col-blog-content blog-main">
      <h1 className="blog-post-title">{title}</h1>
      <div className="mb-3">
        <a href={`/blog/archive/${date.getFullYear()}`} className="text-muted">
          {date.toISOString()}
        </a>
        <a href={`/blog/categories/${category}`} className="badge badge-primary ml-2">
          {category}
        </a>
        {tags.map(tag => (
          <a href={`/blog/tags/${tag}`} className="badge badge-warning">
            {tag}
          </a>
        ))}
        {hidden && <span className="badge badge-danger">Hidden</span>}
        <img
          src="https://hitcounter.pythonanywhere.com/count/tag.svg"
          alt="Hits"
          className="post-hits"
        />
      </div>
      <p className="lead">{description}</p>
      <hr className="mt-3 mb-0" />

      {githubRepository !== null && (
        <>
          <div className="github-summary py-3 d-block text-center">
            <a className="repo-name stretched-link" href="{{ github_repo.html_url }}">
              <img src="/assets/img/github-icon.png" alt="GitHub Icon" />
              <span className="ml-2">{githubRepository}</span>
            </a>

            <div className="repo-stats">
              <img
                alt="GitHub stars"
                src={`https://img.shields.io/github/stars/${githubRepository}?style=social`}
              />
              <img
                alt="GitHub forks"
                src={`https://img.shields.io/github/forks/${githubRepository}?style=social`}
              />
              <img
                alt="GitHub top language"
                src={`https://img.shields.io/github/languages/top/${githubRepository}`}
              />
            </div>
          </div>
          <hr className="my-0" />
        </>
      )}

      <div className="post-content mt-3">
        <Body />
      </div>

      {/* <nav className="blog-pagination text-center mb-5 mt-4">
              {% if prev_and_next['prev'] is not none %}
                  <a className="btn btn-outline-primary mt-1" href="{{ url_for('blog_post', path=prev_and_next['prev'].path) }}">&larr; {{ prev_and_next['prev'].title | truncate(30,true,'...') }}</a>
              {% endif %}
              {% if prev_and_next['next'] is not none %}
                  <a className="btn btn-outline-primary mt-1" href="{{ url_for('blog_post', path=prev_and_next['next'].path) }}">{{ prev_and_next['next'].title | truncate(30,true,'...') }} &rarr;</a>
              {% endif %}
          </nav>

          {% if site_config.disqus_shortname %}
          <div id="disqus_thread"></div>
          <script>
              var disqus_config = function() {
                  this.page.url = '{{ site_config.url + request.path }}'; // Your page's canonical URL variable
                  this.page.identifier = '{{ site_config.url + request.path }}'; // Your page's unique identifier variable
              };
              (function() {
                  var d = document,
                      s = d.createElement('script');
                  s.src = '//{{site_config.disqus_shortname}}.disqus.com/embed.js';
                  s.setAttribute('data-timestamp', +new Date());
                  (d.head || d.body).appendChild(s);
              })();
          </script>
          <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>
          {% endif %} */}
    </div>
  );
};

const BlogPost = ({ data }) => {
  const {
    title,
    date,
    category,
    tags,
    hidden,
    githubRepository,
    description
  } = data.markdownRemark.frontmatter;

  const body = () => <div dangerouslySetInnerHTML={{ __html: data.markdownRemark.html }} />;

  return (
    <Base>
      <BlogBase>
        <BlogPostTemplate
          title={title}
          date={date}
          category={category}
          tags={tags}
          hidden={hidden}
          githubRepository={githubRepository}
          description={description}
          body={body}
        />
      </BlogBase>
    </Base>
  );
};

export default BlogPost;

export const pageQuery = graphql`
  query BlogPostByID($id: String!) {
    markdownRemark(id: { eq: $id }) {
      id
      html
      frontmatter {
        title
        date
        category
        tags
        hidden
        githubRepository
        description
      }
    }
  }
`;
