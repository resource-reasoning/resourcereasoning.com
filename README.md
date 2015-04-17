Resource Reasoning Website
==========================

[![Build Status](https://travis-ci.org/resource-reasoning/resourcereasoning.com.svg)](https://travis-ci.org/resource-reasoning/resourcereasoning.com) (If this icon turns grey or red, something technical has gone wrong, or there are dead links on the website)

Editing the website
-------------------
Site maintainers may edit the site using the interface provided at http://www.resourcereasoning.com/edit/. Once this interface has been authorized with GitHub (click the green buttons). You'll be presented with a listing of the files available to edit on the webiste.

Two types of files are primarily used to generate the website:
* .md files are written in the **Markdown** formatting language. I recommend reading this [brief guide](https://guides.github.com/features/mastering-markdown/) to introduce you to the basics.
* .json files are sets of data records used to build more complex pages such as people and papers. You should be presented with a form interface to make changes to these files.
Both file types have a fairly natural plain-text format and should be reasonably easy to follow by example.

Site maintainers may also accept relevant Issue reports and Pull Requests submitted to the main repository.

Website Structure
-----------------
The main files of interest for editing are:
  * **news.md** ([edit](https://github.com/resource-reasoning/resourcereasoning.com/edit/gh-pages/news.md)) The news page.
    It should be apparent the general format of this file: use second level headers for the month and year, and
    unordered lists for events occuring in that month. A second level of list may be used, eg for POPL.

    The house style is reasonably formal, including links where available.
    All entries should be in the _present tense_.

  * **people.md** ([edit](https://github.com/resource-reasoning/resourcereasoning.com/edit/gh-pages/people.md)) The people page
    This file contains the people directly associated with the Resource Reasoning grant at present and in the past.
    It should be quite easy to see how to change this to add and remove people, change institutions, websites _etc._.
    People should be ordered alphabetically by surname.

    Template person record, use the second format if they have no website.
     ```md
     * [Name Name](http://www.example.com/) (Institution A, Institution B)
     * Name Name (Institution A, Institution B)
     ```

  * Inside the folder **_data**:
    * **papers.json** ([edit](https://github.com/resource-reasoning/resourcereasoning.com/edit/gh-pages/_data/papers.json)) The publications page data
    
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

Files that are less likely to require editing:
  * **index.md** The main page.
    Front page text.
  * **_layouts/page.html** Page template
  * **_layouts/index.html** Index page template
    Images for the gallery should be stored in `images` and referenced as the existing images are inside the page.
  * **_include/nav.html** Common navigational elements.
    You might want to change this page if you add or remove pages from the site, so that all of the other pages link to them.
  * **_include/foot.html** Common page footer.
    This just contains a link to the site maintainence information page.

User Permissions
----------------
Members of the [resource-reasoning/resourcereasoning.com](https://github.com/orgs/resource-reasoning/teams/resourcereasoning-com) Team have admin access to the website. Further administrators can be added there.

Technical Detail
----------------
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

Local Testing
-------------
If you wish to test the site locally, ensure you have ruby installed, and then initially run:
```
gem install bundle
bundle install
```

And to start a local webserver that remakes files whenever changed:
```
bundle exec rake serve
```

You can test for dead links and html errors using:
```
bundle exec rake test
```

Depoloyment Details
-------------------
The site is deployed using [GitHub Pages](https://help.github.com/categories/github-pages-basics/). We additionally use
[Travis CI](https://travis-ci.org/resource-reasoning/resourcereasoning.com) to automatically test that the site builds
and that external links still resolve.
The domain name `resourcereasoning.com` is registered till 21st January 2016 to Thomas Dinsdale-Young.
