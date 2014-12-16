#!/usr/bin/python
import cgi
from datetime import *
import sys
sys.path.append("/vol/rr/rr-web/lib/python")
import rrcgi
import psycopg2


data = cgi.FieldStorage()

conn = psycopg2.connect(rrcgi.connect_string)
cur = conn.cursor()

paperid = int(data.getvalue("id"))

if "delete" in data:
	cur.execute("UPDATE papers SET deleted=TRUE WHERE paperid=%s;", (paperid,))
	conn.commit()

if "update" in data:
	try:
		pubdate = datetime.strptime(data.getvalue("pubdate"), "%Y-%m-%d").date()
	except ValueError:
		pubdate = date.today()
	cur.execute("UPDATE papers SET title=%s, pubdate=%s, authors=%s, venue=%s, bibtex=%s, pdf=%s, ps=%s, pdflong=%s, pslong=%s, display=%s, submittedby=%s, abstract=%s WHERE paperid=%s;", ( data.getvalue("title"), pubdate, data.getvalue("authors"), data.getvalue("venue"), data.getvalue("bibtex"), data.getvalue("pdf"), data.getvalue("ps"), data.getvalue("pdffull"), data.getvalue("psfull"), "display" in data, data.getvalue("submittedby"), data.getvalue("abstract"),paperid))
	conn.commit()

cur.execute("SELECT paperid, display, deleted, title, pubdate, authors, venue, bibtex, pdf, ps, pdflong, pslong, submittedby, abstract FROM papers WHERE paperid=%s;", (paperid,))

content = ""

items = ["title", "pubdate", "authors", "venue", "bibtex", "pdf", "ps", "pdffull", "psfull", "submittedby", "abstract"]

for res in cur:
	content = """<?xml version="1.0" encoding="utf-8" ?>
<paper id="%d" display="%s" deleted="%s">""" % res[0:3]
	for i in range(0, len(items)):
		if res[i + 3] != None:
			if type(res[i + 3]) == date:
				content += "<" + items[i] + "><![CDATA[" + res[i + 3].strftime("%Y-%m-%d") + "]]></" + items[i] + ">\n"
			else:
				content += "<" + items[i] + "><![CDATA[" + res[i + 3] + "]]></" + items[i] + ">\n"

	content += "</paper>"
cur.close()
conn.close()

print "Content-Type: text/xml; utf-8"
print
print content


# cgi.test()
