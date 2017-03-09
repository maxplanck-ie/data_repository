.PHONY: all chmod

all: FASTA LIFTOVER chmod

FASTA: Lambda.fa PhiX174.fa ERCC92.fa

LIFTOVER: liftOver/dm3ToDm6.over.chain.gz liftOver/dm6ToDm3.over.chain.gz

chmod:
	chmod -R a+r .

ERCC92.fa:
	wget --quiet "http://media.invitrogen.com.edgesuite.net/softwares/ERCC92.fa"

PhiX174.fa:
	wget --quiet -O - "http://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?tool=portal&sendto=on&log$=seqview&db=nuccore&dopt=fasta&val=9626372&extrafeat=0&maxplex=1" > PhiX174.fa

Lambda.fa:
	wget --quiet -O - "http://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?tool=portal&sendto=on&log$=seqview&db=nuccore&dopt=fasta&val=215104&extrafeat=0&maxplex=1" > Lambda.fa

liftOver:
	mkdir liftOver

liftOver/dm3ToDm6.over.chain.gz: liftOver
	wget --quiet -P liftOver http://hgdownload.soe.ucsc.edu/goldenPath/dm3/liftOver/dm3ToDm6.over.chain.gz

liftOver/dm6ToDm3.over.chain.gz: liftOver
	wget --quiet -P liftOver http://hgdownload.soe.ucsc.edu/goldenPath/dm6/liftOver/dm6ToDm3.over.chain.gz

liftOver/mm10ToMm9.over.chain.gz: liftOver
	wget --quiet -P liftOver http://hgdownload.soe.ucsc.edu/goldenPath/mm10/liftOver/mm10ToMm9.over.chain.gz

liftOver/mm9ToMm10.over.chain.gz: liftOver
	wget --quiet -P liftOver http://hgdownload.soe.ucsc.edu/goldenPath/mm9/liftOver/mm9ToMm10.over.chain.gz
