HTMLS = index.html news.html people.html support.html addpaper.html
DEPS = nav.html foot.html
SSI = /vol/rr/rr-web/bin/ssi.py
OUTDIR = /vol/rr/www

all : dist

dist : $(HTMLS)
	cp -t $(OUTDIR) $(HTMLS)

clean :
	rm $(HTMLS)

$(HTMLS) : %.html : %.shtml $(DEPS)
	$(SSI) $< $@
