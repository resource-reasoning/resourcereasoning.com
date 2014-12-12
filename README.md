Resource Reasoning Website
==========================
The resource reasoning website is at http://www.resourcereasoning.com/, and is intended as the public web presence for the Resource Reasoning grant.
The actual address of the webserver is http://www-rr.doc.ic.ac.uk/.
HTTPS is also supported on the server, and is used for the interface for maintaining publications.

Editing the website
-------------------
The _live_ website is located at `/vol/rr/www` on the shared volume.
For changes to the static content, you usually _do not want to modify this_.
Instead, modify the corresponding `.shtml` files located in `/vol/rr/rr-web/src` and run `make` which will process some includes and copy the result to the live site.
Be careful not to edit the `.html` files as they are automatically generated, and will be clobbered.

The main files of interest for editing in `/vol/rr/rr-web/src` are:
  * **index.shtml** The main page.
    You might want to edit the blurb or change the pictures in the photo gallery.
    Images for the gallery should be stored in `/vol/rr/www/images` and referenced as the existing images are inside the page.
  * **news.shtml** The news page.
    It should be apparent the general format of this file: the main body consists of `div` elemnts of class `newsdate`, containing the month and year of the immediately subsequent news items, each of which occupies a `newsitem`-class `div`.
    The house style is reasonably formal, including links where available.
    All entries should be in the _present tense_.
  * **people.shtml** The people page.
    This page lists the people directly associated with the Resource Reasoning grant at present.
    They are stored in a JavaScript array of objects, and the list is dynamically generated (allowing it to be reformatted by institution as desired).
    It should be quite easy to see how to change this to add and remove people, change institutions, websites _etc._.
    I like to maintain the JavaScript-free list in the page (just in case...), usually by copying the generated html from a browser.
  * **support.shtml** The support page.
    Should be self-explanatory.
  * **nav.html** Common navigational elements.
    You might want to change this page if you add or remove pages from the site, so that all of the other pages link to them.
    This file is included by both dynamically- and statically-generated pages.
  * **foot.html** Common page footer.
    This just contains a link to the site maintainer.
    If you're taking over maintenance of the site _change this to you_.

Some other files in `/vol/rr/www` you might want or need to modify include:
  * **styles.css** The main style file.
  * **papers.cgi** Python file that dynamically generates the list of publications.
  * **submitpaper.cgi** The paper submission form.

In fact, you _should_ edit the last of these, as it automatically generates an e-mail when someone submits a paper.
You should update it so that it e-mails you.

The dynamic list of papers is stored in a database.
The connect string for the database is located in `/vol/rr/rr-web/lib/python/rrcgi.py`.
CGI error logs are stored in `/vol/rr/rr-web/log`.
(I seem to remember some potential caveats to do with the owner of pyc/group of pyc files.
CGI scripts will be executed by the user `rr_u` in the group `rr`, and may have trouble if they cannot use/overwrite the compiled python.)

There is a web interface for editing the papers at https://www-rr.doc.ic.ac.uk/ed/papers.cgi.
Anyone in the `rr` group can sign in and access this.
(Note, it would be a good idea to fix this to use local copies of jquery scripts...).
Papers are not published to the list until you authorise them.
I recommend having a look at the style of other entries to normalise new submissions.
For instance, conference names are generally formatted as "POPL 2012" or "ESOP 2013".
Names are a comma-separated list, with no "and".
Check the abstract for funny characters, and use `<p>` elements to break up paragraphs.

The editorial policy is not to allow papers that have yet to be published.
(You don't need to delete them, just don't put them up until publication.)
Workshop papers and techreports are generally not included, although often an "extended version" can accompany a paper.
It's good to have the BibTeX where possible.

The domain name `resourcereasoning.com` is registered till 21st January 2016.
If you need it beyond then, I can renew it.
