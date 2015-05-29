.PHONY: all chmod

all: FASTA chmod

FASTA: Lambda.fa PhiX174.fa ERCC92.fa

chmod:
	chmod a+r *

ERCC92.fa:
	wget --quiet "http://media.invitrogen.com.edgesuite.net/softwares/ERCC92.fa"

PhiX174.fa:
	wget --quiet -O - "http://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?tool=portal&sendto=on&log$=seqview&db=nuccore&dopt=fasta&val=9626372&extrafeat=0&maxplex=1" > PhiX174.fa

Lambda.fa:
	wget --quiet -O - "http://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?tool=portal&sendto=on&log$=seqview&db=nuccore&dopt=fasta&val=215104&extrafeat=0&maxplex=1" > Lambda.fa
