function edit(id) {
	$.ajax( {cache: false,
	       	dataType: "xml",
		data: {id : id},
		url : "ed/pquery.cgi",
		success: function(data) {
			var jdata = $(data.documentElement);
			var theform = $('<form action="ed/pquery.cgi" method="post" onsubmit="return validate(this)"><input type="hidden" name="id" /><label for="title">Title</label> <input type="text" name="title" size="80" /><br /><label for="authors">Authors</label> <input type="text" name="authors" size="80" /><br /><label for="venue">Venue</label> <input type="text" name="venue" size="80" /><br /><label for="pubdate">Publication date</label> <input type="text" name="pubdate" size="10" id="datepicker" /><br /><label for="pdf">PDF link</label> <input type="text" name="pdf" size="80" /><br /><label for="ps">PS link</label> <input type="text" name="ps" size="80" /><br /><label for="pdffull">PDF link (full version)</label> <input type="text" name="pdffull" size="80" /><br /><label for="psfull">PS link (full version)</label> <input type="text" name="psfull" size="80" /><br /><label for="abstract">Abstract</label><textarea name="abstract" rows="10" cols="80"></textarea><br /><label for="bibtex">BibTeX</label><textarea name="bibtex" rows="10" cols="80"></textarea><br /><label for="submittedby">Contributor</label> <input type="text" name="submittedby" size="60"/><br /><input type="checkbox" name="display" value="true" /><label for="display">Publish</label><br /><button type="submit" name="update" value="true">Update</button><button type="button" onclick="deletePaper(this)">Delete</button><button type="button" onclick="cancel(this)">Cancel</button></form>');
			var fields = ["title", "pubdate", "authors", "venue", "pubdate", "pdf", "ps", "pdffull", "psfull", "submittedby", "abstract", "bibtex"];
			for (var f in fields) {
				theform.find('[name="' + fields[f] + '"]').attr("value", jdata.find(fields[f]).text());
			}
			if (jdata.attr('display').toLowerCase() === 'true') {
				theform.find('[name="display"]').attr("checked", true);
			}
			theform.find('[name="pubdate"]').datepicker({ dateFormat : 'yy-mm-dd' })
				.datepicker("setDate", jdata.find("pubdate").text());
			theform.find('[name="id"]').attr("value", id);
			theform.ajaxForm(updatePaper);
			var paper = $("#paper" + id);
			paper.contents().remove();
			paper.append(theform);
		}
	});
}

function updatePaper(data) {
	var jdata = $(data.documentElement);
	var id = jdata.attr('id');
	if (jdata.attr('deleted').toLowerCase() === 'true') {
		$("#paper" + id).next().andSelf().remove();
		return;
	}
		
	var titleclass = jdata.attr('display').toLowerCase() === 'true' ? 'displayed' : 'undisplayed';
	var title = jdata.find('title').text();
	var links = '';
	if (jdata.find('pdf').length) {
		links += '[<a href="' + jdata.find('pdf').text() + '">PDF</a>] ';
	}
	if (jdata.find('ps').length) {
		links += '[<a href="' + jdata.find('ps').text() + '">PS</a>] ';
	}
	if (jdata.find('pdffull, psfull').length) {
		links += 'full: ';
		if (jdata.find('pdffull').length) {
			links += '[<a href="' + jdata.find('pdffull').text() + '">PDF</a>] ';
		}
		if (jdata.find('psfull').length) {
			links += '[<a href="' + jdata.find('psfull').text() + '">PS</a>] ';
		}
	}
	$("#bibtex" + id).remove();
	if (jdata.find('bibtex').length) {
		$('<pre id="bibtex' + id + '">' + (jdata.find('bibtex').text().replace(/&/g,'&amp;').                                         
                replace(/>/g,'&gt;').                                           
                replace(/</g,'&lt;').                                           
                replace(/"/g,'&quot;') )
			       	+ '</pre>').dialog({width : 600, title : "BibTeX", autoOpen : false});
		links += '[<a href="javascript:dobib(' + id + ')">BibTeX</a>]';
	}

	var thepaper = $('<a name="' + id + '"><span class="papertitle ' + titleclass + '">' + title + '</span></a><span class="links">' + links + '</span><br><a href="javascript:edit(' + id + ')">edit</a><div class="paperbody"><p class="authors">' + jdata.find('authors').text() + '</p><p class="publishedin">' + jdata.find('venue').text() + '</p><div class="abstract">' + jdata.find('abstract').text() + '</div></div>');

	$("<a href=\"#\">show abstract</a>")
	.addClass('abstractlink')
	.insertBefore(thepaper.find(".abstract").hide())
	.click(function() {
		$(this).next().toggle();
		if ($(this).text() == "show abstract") {
			$(this).text("hide abstract");
		} else {
			$(this).text("show abstract");
		}
		return false;
	});

	var paper = $("#paper" + id);
	paper.contents().remove();
	paper.append(thepaper);
}

function cancel(button) {
	var id = $(button).parent().find('[name="id"]').attr("value");
	$.ajax( {cache : false,
		dataType : "xml",
		data: {id : id},
		url : "ed/pquery.cgi",
		success: updatePaper
	});
}

function deletePaper(button) {
	var id = $(button).parent().find('[name="id"]').attr("value");
	$("<div>Are you sure you wish to delete this paper?</div>").dialog({
		buttons : {
			"No" : function() {
				$(this).dialog("close");
			},
			"Yes" : function() {
				$(this).dialog("close");
				$.ajax( {cache: false, dataType: "xml", data: {id:id, delete:true}, url : "ed/pquery.cgi", success: updatePaper} )
			}},
		title : 'Confirm Deletion',
		modal : true
	});
}


			function missingDialog(omission) {
				$('<div style="font-size:smaller">Please fill out ' + omission + ".</div>").dialog({title : 'Missing Information'});
			}

			function validate(form) {
				fields = ["title", "authors", "venue", "pubdate", "abstract", "submittedby"];
				fieldName = ["the paper title", "the paper authors", "the publication venue", "the publication date", "the paper abstract", "your contact information"];
				for (var f in fields) {
					field = form[fields[f]];
					if (field.value === null || field.value === "") {
						field.focus();
						missingDialog(fieldName[f]);
						return false;
					}
				}
				if ((form.pdf.value === null || form.pdf.value === "") && (form.ps.value === null || form.ps.value === "")) {
					form.pdf.focus();
					missingDialog("the PDF or PS link");
					return false;
				}
				var thedate = $("#datepicker").datepicker("getDate");
				var datebits = form.pubdate.value.split("-");
				if (!( datebits[0] == thedate.getFullYear() && datebits[1] == (thedate.getMonth()+1) && datebits[2] == thedate.getDate()) ) {
					form.pubdate.focus();
					missingDialog("the publication date with a valid date");
					return false;
				}
			}

