#!/usr/bin/python
import cgi
import sys

sys.path.append("/vol/rr/rr-web/lib/python")
import rrcgi

import psycopg2

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
cur = conn.cursor();

cur.execute("SELECT title, pdf, ps, pdflong, pslong, authors, venue, abstract, paperid, bibtex FROM papers WHERE deleted=FALSE and display=TRUE ORDER BY pubdate DESC;")

content = """<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>Publications - Resource Reasoning</title>
		<link type="text/css" href="styles.css" rel="stylesheet" />
		<style type="text/css">
			.papertitle {font-weight: bold; font-size: larger}
			.paperbody {margin-left: 1em;}
			.authors {margin:0.2em}
			.publishedin {margin:0.2em; margin-bottom:0.1em;margin-left:2em;font-style: italic}
			.abstract {font-size: smaller; text-align: justify; max-width:40em; margin-top:0.1em;margin-left:2em}
                        .abstract p {margin-top:0em; margin-bottom:0.5em}
                        .abstract p+p {text-indent:2em}
			.links {font-size: smaller; margin-left: 1em; display:block; float:right; margin-right:100px; margin-top:0.3em}
			.abstractlink {font-size: smaller; margin-left:2em}
			.bibtex {font-size: small; display:none}
		</style>
		<link rel="shortcut icon" href="favicon.ico" />
		<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js"></script>
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

content += rrcgi.ssi("nav.html")

content += """			<div id="content">

				<h1>Publications</h1>
				<p>The following is a list of recent publications by the Resource Reasoning group:</p>
"""

paper = """				<div class="paper">
					<span class="papertitle">%s</span>
					<span class="links">%s</span>
					<div class="paperbody">
						<p class="authors">%s</p>
						<p class="publishedin">%s</p>
						<div class="abstract">%s
						</div>
					</div>
					%s
				</div>
"""

#results = cur.fetchall()
for res in cur:
	content += paper % (res[0], make_links(res[1], res[2], res[3], res[4], res[8] if res[9] != None and res[9] != "" else None), res[5], res[6], res[7], ( ('<pre class="bibtex" id="bibtex%s">' % res[8]) + cgi.escape(res[9]) + '</pre>' if res[9]!=None and res[9]!="" else ''))

content += """				<p>To add a publication to this list, please fill out <a href="addpaper.html">this form</a>.</p>
			</div>
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
