# Nitratine.net

Based off https://github.com/netlify-templates/gatsby-starter-netlify-cms

### Launch

- Remove robots
- `UA-117153268-6` => `UA-117153268-2`
- Enabled AdSense and `static.useInternalLinking`=`non-post-associations`

### Not Required (after launch)

- Group tags/categories/years at top of category pages as links to headers (with numbers) e.g. taga (2) tagb (5) tagc (8)
- MEDIUM: Query typings throughout
- BUG: Some images aren't linked to original
- SMALL: Put actual react-bootstrap components in
- SMALL: Add switch to disable ads on particular pages
- MAYBE: Create a language on top of python that allows for some extra tokens?
- MAYBE: Config for footer?

### Eventually...

Setup CMS OAuth without netlify:

- https://github.com/vencax/netlify-cms-github-oauth-provider
- https://tylergaw.com/articles/netlify-cms-custom-oath-provider/
