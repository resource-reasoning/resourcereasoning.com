#!/usr/bin/python
import cgi
import sys
sys.path.append("/vol/rr/rr-web/lib/python")
import rrcgi
import psycopg2
import os

def make_links(pdf,ps,pdffull,psfull,bibid):
	links = ""
	link = '[<a href="%s">%s</a>] '
	if (pdf != None and pdf != ""):
		links += link % (pdf, "PDF")
	if (ps != None and ps != ""):
		links += link % (ps, "PS")
	if ((psfull != None and psfull != "") or (pdffull != None and pdffull != "")):
		links += "full: "
		if (pdffull !=None and pdffull != ""):
			links += link % (pdffull, "PDF")
		if (psfull != None and psfull != ""):
			links += link % (psfull, "PS")
	if (bibid != None):
		links += '[<a href="javascript:dobib(' + str(bibid) + ')">BibTeX</a>]'
	return links


conn = psycopg2.connect(rrcgi.connect_string)
cur = conn.cursor()

cur.execute("SELECT title, pdf, ps, pdflong, pslong, authors, venue, abstract, paperid, display, bibtex FROM papers WHERE deleted=FALSE ORDER BY pubdate DESC;")

content = """<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>Papers (Editor Interface) - Resource Reasoning</title>
		<base href="https://""" + os.environ["HTTP_HOST"] + """/" />
		<link type="text/css" href="styles.css" rel="stylesheet" />
		<style type="text/css">
			.papertitle {font-weight: bold; font-size: larger;}
			.undisplayed {font-style: italic; color: grey}
			.paperbody {margin-left: 1em;}
			.authors {margin:0.2em}
			.publishedin {margin:0.2em; margin-bottom:0.1em;margin-left:2em;font-style: italic}
			.abstract {font-size: smaller; text-align: justify; max-width:40em; margin-top:0.1em;margin-left:2em}
			.abstract p {margin-top:0em; margin-bottom:0.5em}
			.abstract p+p {text-indent:2em}
			.links {font-size: smaller; margin-left: 1em; display:block; float:right; margin-right: 100px}
			.abstractlink {font-size: smaller; margin-left:2em}
			label {width : 12em; float : left; text-align: left; margin-right: 0.5em; display:block; font-size:smaller }
		</style>
		<link rel="shortcut icon" href="favicon.ico" />
		<!-- <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/> -->
		<link href="css/jquery-ui.css" rel="stylesheet" type="text/css"/>
		<!-- <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script> -->
		<!-- <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js"></script> -->
		<script type="text/javascript" src="scripts/jquery-1.4.2.min.js"></script>
		<script type="text/javascript" src="scripts/jquery-ui.min.js"></script>
		<script type="text/javascript" src="scripts/jquery.form.js"></script>
		<script type="text/javascript" src="ed/paperedit.js"></script>
		<script type="text/javascript"><!--
			$(document).ready(function(){
				$("<a href=\\"#\\">show abstract</a>")
					.addClass('abstractlink')
					.insertBefore($(".abstract").hide())
					.click(function() {
						$(this).next().toggle();
							if ($(this).text() == "show abstract") {
								$(this).text("hide abstract");
							} else {
								$(this).text("show abstract");
							}
							return false;
					});
				$(".bibtex").dialog({width : 600, title : "BibTeX", autoOpen : false});
			});
			function dobib(id) {
				$("#bibtex" + id).dialog("open");
			} //-->
		</script>
	</head>
	<body>
		<div id="main">
"""

content += rrcgi.ssi("nav.html");

content += """			<div id="content">

				<h1>Papers</h1>
"""

paper = """				<div class="paper" id="paper%(id)s">
					<a name="%(id)s"><span class="papertitle %(class)s">%(title)s</span></a>
					<span class="links">%(links)s</span><br>
					<a href="javascript:edit(%(id)s)">edit</a>
					<div class="paperbody">
						<p class="authors">%(authors)s</p>
						<p class="publishedin">%(venue)s</p>
						<div class="abstract">%(abstract)s
						</div>
						%(bibtex)s
					</div>
				</div>
				<hr/>
"""

#results = cur.fetchall()
for res in cur:
	content += paper % {
			"title" : res[0],
			"links" : make_links(res[1], res[2], res[3], res[4], res[8] if res[10]!=None and res[10]!="" else None),
			"authors" : res[5],
			"venue" : res[6],
			"abstract" : res[7],
			"id" : res[8],
			"class" : ( "displayed" if res[9] else "undisplayed"),
			"bibtex" : ( ('<pre class="bibtex" id="bibtex%s">' % res[8]) + cgi.escape(res[10]) + '</pre>' if res[10]!=None and res[10]!="" else '')}
	
#	(res[0], make_links(res[1], res[2], res[3], res[4]), res[5], res[6], res[7])

content += """			</div>
		</div>
"""
content += rrcgi.ssi("foot.html")
content += """	</body>
</html>
"""



print "Content-Type: text/html; utf-8"
print
print content


# cgi.test()
