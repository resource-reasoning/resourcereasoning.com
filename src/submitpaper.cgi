#!/usr/bin/python
import cgi
from datetime import *
import sys
sys.path.append("/vol/rr/rr-web/lib/python")
import rrcgi
import psycopg2

import smtplib
from email.mime.text import MIMEText

def make_links(pdf,ps,pdffull,psfull):
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
	return links

content = """<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
        <head>
                <title>Paper Submission - Resource Reasoning</title>
                <link type="text/css" href="styles.css" rel="stylesheet" />
                <style type="text/css">
                        .papertitle {font-weight: bold; font-size: larger}
                        .paperbody {margin-left: 1em;}
                        .authors {margin:0.2em}
                        .publishedin {margin:0.2em; margin-bottom:0.1em;margin-left:2em;font-style: italic}
                        .abstract {font-size: smaller; text-align: justify; max-width:40em; margin-top:0.1em;margin-left:2em}
                        .links {font-size: smaller; margin-left: 1em}
                        .abstractlink {font-size: smaller; margin-left:2em}
                </style>
                <link rel="shortcut icon" href="favicon.ico" />
                <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>

                <!--<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js"></script>-->
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

                        }); //-->
                </script>
        </head>
        <body>
                <div id="main">
"""

content += rrcgi.ssi("nav.html")



form = cgi.FieldStorage()

if form.getvalue("submittedby") == None or form.getvalue("submittedby").find("@") < 1:
        content += """<div id="content"><p>Please supply your e-mail address in the contact field.</p>"""
        content += """</div></div></html>"""
        print "Content-Type: text/html; utf-8"
        print
        print content
        exit()

# Store paper in database

conn = psycopg2.connect(rrcgi.connect_string)
cur = conn.cursor()

try:
	pubdate = datetime.strptime(form.getvalue("pubdate"), "%Y-%m-%d").date()
except ValueError:
	pubdate = date.today()

cur.execute("INSERT INTO papers (title, pubdate, authors, venue, bibtex, pdf, ps, pdflong, pslong, display, deleted, submittedby, abstract) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE, FALSE, %s, %s);", ( form.getvalue("title"), pubdate, form.getvalue("authors"), form.getvalue("venue"), form.getvalue("bibtex"), form.getvalue("pdf"), form.getvalue("ps"), form.getvalue("pdffull"), form.getvalue("psfull"), form.getvalue("submittedby"), form.getvalue("abstract")))

conn.commit()

cur.execute("SELECT currval('papers_paperid_seq');")
paperid = cur.fetchone()

cur.close()
conn.close()

# Send notification e-mail

rcpt = "gds@doc.ic.ac.uk"
sndr = rcpt

mailtext = """A new paper has been submitted to the Resource Reasoning website for review.

Edit: https://www-rr.doc.ic.ac.uk/ed/papers.cgi#paper%d
Contact: %s
Title: %s
Authors: %s
Venue: %s
Publication Date: %s
PDF: %s
PS: %s
PDF (long): %s
PS (long): %s
Abstract:
%s

BibTeX:
%s
""" % (paperid[0], form.getvalue("submittedby"), form.getvalue("title"), form.getvalue("authors"), form.getvalue("venue"), form.getvalue("pubdate"), form.getvalue("pdf"), form.getvalue("ps"), form.getvalue("pdffull"), form.getvalue("psfull"), form.getvalue("abstract"), form.getvalue("bibtex"))

msg = MIMEText(mailtext);
msg['Subject'] = "Resource Reasoning - Paper Submitted (%d)" % paperid
msg['From'] = sndr
msg['To'] = rcpt

s = smtplib.SMTP('smarthost.cc.ic.ac.uk')
s.mail(sndr)
s.rcpt(rcpt)
s.data(msg.as_string())
s.quit()

# cur.execute("SELECT title, pdf, authors, venue, abstract FROM papers WHERE deleted=FALSE and display=TRUE ORDER BY pubdate DESC;")

content += """			<div id="content">

				<h1>Paper Submission</h1>
				<p>You have submitted the following paper:</p>
"""

paper = """				<div class="paper">
					<span class="papertitle">%s</span>
					<span class="links">%s</span>
					<div class="paperbody">
						<p class="authors">%s</p>
						<p class="publishedin">%s</p>
						<p class="abstract">%s
						</p>
					</div>
				</div>
"""

# results = cur.fetchall()
# for res in results:
# 	content += paper % res

content += paper % (form.getvalue("title"), make_links(form.getvalue("pdf"), form.getvalue("ps"), form.getvalue("pdffull"), form.getvalue("psfull")), form.getvalue("authors"), form.getvalue("venue"), form.getvalue("abstract"))

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
