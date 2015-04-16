.PHONY:	all

all: nr/nr.31.pog nt/nt.27.pog

nr/nr.31.pog:
	mkdir -p nr
	chmod a+rx nr
	cd nr; wget -r -np -nH -nd -A 'nr*.tar.gz' ftp://ftp.ncbi.nlm.nih.gov/blast/db/
	cd nr; for f in *.tar.gz; do tar xf $$f; rm $$f; done
	chmod a+r nr/*
	echo "Downloaded on:" > nr/version.txt
	date >> nr/version.txt

nt/nt.27.pog:
	mkdir -p nt
	chmod a+rx nt
	cd nt; wget -r -np -nH -nd -A 'nt*.tar.gz' ftp://ftp.ncbi.nlm.nih.gov/blast/db/
	cd nt; for f in *.tar.gz; do tar xf $$f; rm $$f; done
	chmod a+r nt/*
	echo "Downloaded on:" > nt/version.txt
	date >> nt/version.txt
