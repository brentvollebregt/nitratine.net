import React from "react";

interface IComments {}

const Comments: React.FC<IComments> = ({}) => {
  // TODO gatsby-plugin-disqus
  return (
    <div>
      TODO Disqus Comments
      {/* 
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
        {% endif %} 
      */}
    </div>
  );
};

export default Comments;
