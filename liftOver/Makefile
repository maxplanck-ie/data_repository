targets=\
	hg38ToHg19.over.chain \
	hg19ToHg38.over.chain \
	mm10ToMm9.over.chain \
	mm9ToMm10.over.chain \
	dm6ToDm3.over.chain \
	dm3ToDm6.over.chain \
	danRer10ToDanRer7.over.chain \
	danRer7ToDanRer10.over.chain

.PHONY: all chmod

all: ${targets} chmod

chmod:
	chmod a+r *

%.over.chain:
	$(eval bname = $(word 1,$(subst To,  ,$@)))
	wget -O - http://hgdownload.cse.ucsc.edu/goldenPath/${bname}/liftOver/$@.gz | zcat > $@
