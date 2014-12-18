Resource Reasoning Website
==========================

Editing the website
-------------------
The preferred method of contributing to the site is by pull request, or if you have commit rights, directly pushing your
changes to the live repository.

Site maintainers will also accept Issue reports submitted to the main repository.

The site is built on the [GitHub Pages](https://help.github.com/categories/github-pages-basics/) platform, which is
backed by the [Jekyll](http://jekyllrb.com/) website framework. Pages can be written using
[Markdown](http://daringfireball.net/projects/markdown/) (preferred) or HTML, and there
is a powerful [templating language](http://jekyllrb.com/docs/templates/) available for use.

Pages to be interpreted by the Jekyll framework should be started with a YAML variable block, for example:
```
---
title: Page Name
---
```
The main content of the page should then follow.

Any other files present in the directory structure (except for those prefixed with `_`, `.`, or explicitly excluded in
`_config.yml`) will be published unchanged to the website.

The main files of interest for editing are:
  * **index.shtml** The main page.
    You might want to edit the blurb or change the pictures in the photo gallery.
    Images for the gallery should be stored in `images` and referenced as the existing images are inside the page.

  * **news.md** The news page.
    It should be apparent the general format of this file: use second level headers for the month and year, and
    unordered lists for events occuring in that month. A second level of list may be used, eg for POPL.

    The house style is reasonably formal, including links where available.
    All entries should be in the _present tense_.

  * **_data/people.yaml** The people page data
    This file contains the people directly associated with the Resource Reasoning grant at present and in the past.
    It should be quite easy to see how to change this to add and remove people, change institutions, websites _etc._.

  * **_data/papers.yaml** The publications page data
    This file contains the data of publications, fields should be reasonably obvious from the data already in the file.

    Page style guide:
    * Conference names are generally formatted as "POPL 2012" or "ESOP 2013".
    * Names are a comma-separated list, with no "and".
    * The editorial policy is not to allow papers that have yet to be published.
    * Workshop papers and techreports are generally not included, although often an "extended version" can accompany a
        paper using the pdflong/pslong fields.
    * It's good to have the BibTeX where possible.

  * **support.md** The support page.
    Should be self-explanatory.
  * **_include/nav.html** Common navigational elements.
    You might want to change this page if you add or remove pages from the site, so that all of the other pages link to them.
    This file is included by both dynamically- and statically-generated pages.
  * **_include/foot.html** Common page footer.
    This just contains a link to the site maintainence information page.

Depoloyment Details
-------------------
The site is deployed using [GitHub Pages](https://help.github.com/categories/github-pages-basics/). We additionally use
[Travis CI](https://travis-ci.org/resource-reasoning/resourcereasoning.com) to automatically test that the site builds
and that external links still resolve.
The domain name `resourcereasoning.com` is registered till 21st January 2016 to Thomas Dinsdale-Young.
