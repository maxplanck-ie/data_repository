.PHONY: all PERMS

#THIS IS REQUIRED! Otherwise, GTF/BED files are deleted!
.SECONDARY:

all: GENOME GENOMEINDICES TRANSCRIPTOMES OTHER PERMS

PERMS: GENOME GENOMEINDICES TRANSCRIPTOMES OTHER
	../fixPerms.sh

genome_fasta/genome.fa:
	mkdir -p genome_fasta
	wget --quiet -O - $(genome_url) | zcat > $@

genome_fasta/genome.dict: genome_fasta/genome.fa
	java -Xmx2g -jar /package/picard-tools-1.121/CreateSequenceDictionary.jar REFERENCE=genome_fasta/genome.fa OUTPUT=genome_fasta/genome.dict

genome_fasta/genome.fa.fai: genome_fasta/genome.fa
	/package/samtools/samtools faidx genome_fasta/genome.fa

genome_fasta/genome.2bit: genome_fasta/genome.fa
	/package/UCSCtools/faToTwoBit genome_fasta/genome.fa genome_fasta/genome.2bit

genome_fasta/genome.chrom.sizes: genome_fasta/genome.2bit
	/package/UCSCtools/twoBitInfo genome_fasta/genome.2bit stdout | sort -k2rn > genome_fasta/genome.chrom.sizes

#All genome-level indices, excluding those for alignments
GENOME: genome_fasta/genome.chrom.sizes genome_fasta/genome.fa.fai genome_fasta/genome.dict

%.gtf:
	mkdir -p $(dir $@)
ifeq ($(PROT),genePred)
ifeq ($(CONV),)
	wget --quiet -O - http://$(URL) | zcat | cut -f 2- | /package/UCSCTools/genePredToGtf file /dev/stdin $@
else
	wget --quiet -O - http://$(URL) | zcat | cut -f 2- \
	| /package/UCSCTools/genePredToGtf file /dev/stdin /dev/stdout \
	| ../convertChromosomes.py $(CONV) > $@
endif
else ifeq ($(PROT),local)
ifeq ($(CONV),)
	zcat $(URL) > $@
else
	zcat $(URL) ../convertChromosomes.py $(CONV) > $@
endif
else
ifeq ($(CONV),)
	wget --quiet -O - $(PROT)://$(URL) | zcat > $@
else
	wget --quiet -O - $(PROT)://$(URL) | zcat \
	| ../convertChromosomes.py $(CONV) > $@
endif
endif

%.bed: %.gtf
	awk '{if ($$3 != "gene") print $$0;}' $< \
	| grep -v "^#" \
	| /package/UCSCtools/gtfToGenePred /dev/stdin /dev/stdout \
	| /package/UCSCtools/genePredToBed stdin $@

%.slop.gtf: %.gtf
	grep -v "^#" $< \
	| awk 'BEGIN{FS="\t"; OFS="\t"}{if($$3 == "gene" || $$3 == "transcript") {$$4 -= 500; $$5 += 500; if($$4 < 1) {$$4 = 1}; print}}' > $@

%transcript2gene.txt:
	awk '{if ($$3 != "gene") print $$0;}' $(dir $@)genes.gtf \
	| grep -v "^#" \
	| /package/UCSCtools/gtfToGenePred -genePredExt /dev/stdin /dev/stdout \
	| cut -f 1,12 > $(dir $@)transcript2gene.txt

#Note, the `ln` line prevents tophat from duplicating the genome fasta
#Bowtie2 uses the same indices as HISAT
BowtieIndex/genome.rev.2.bt2: HISATIndex/genome.rev.2.bt2
	mkdir -p BowtieIndex
	ln HISATIndex/genome.1.bt2 BowtieIndex/genome.1.bt2
	ln HISATIndex/genome.2.bt2 BowtieIndex/genome.2.bt2
	ln HISATIndex/genome.3.bt2 BowtieIndex/genome.3.bt2
	ln HISATIndex/genome.4.bt2 BowtieIndex/genome.4.bt2
	ln HISATIndex/genome.rev.1.bt2 BowtieIndex/genome.rev.1.bt2
	ln HISATIndex/genome.rev.2.bt2 BowtieIndex/genome.rev.2.bt2
	ln genome_fasta/genome.fa BowtieIndex/genome.fa

#Note, `export` needs to be on the same line, otherwise tophat is run in a different shell
%tophat.rev.2.bt2: BowtieIndex/genome.rev.2.bt2
	mkdir -p $(DIR)/tophat
	export PATH=$$PATH:/package/bowtie2-2.2.3 ;\
	cd $(DIR); \
	/package/tophat-2.0.13.Linux_x86_64/tophat --GTF genes.gtf --transcriptome-index tophat/tophat ../../BowtieIndex/genome
	rm -rf $(DIR)/tophat_out

%HISAT2/splices.txt:
	mkdir -p $(DIR)/HISAT
	~/bin/extract_splice_sites.py $(DIR)/genes.gtf > $(DIR)/HISAT/splices.txt
	mkdir -p $(DIR)/HISAT2
	/package/hisat2-2.0.0-beta/extract_exons.py $(DIR)/genes.gtf > $(DIR)/HISAT2/exons.txt
	/package/hisat2-2.0.0-beta/extract_splice_sites.py $(DIR)/genes.gtf > $(DIR)/HISAT2/splice_sites.txt

HISAT2Index/genome.8.ht2: genome_fasta/genome.fa
	mkdir -p HISAT2Index
	/package/hisat2-2.0.0-beta/hisat2-build -q -p 10 genome_fasta/genome.fa HISAT2Index/genome

HISATIndex/genome.rev.2.bt2: genome_fasta/genome.fa
	mkdir -p HISATIndex
	/package/hisat-0.1.6-beta/bin/hisat-build -q genome_fasta/genome.fa HISATIndex/genome

BWAindex/genome.fa.sa: genome_fasta/genome.fa
	mkdir -p BWAindex
	/package/bwa-0.7.4/bwa index genome_fasta/genome.fa
	mv genome_fasta/genome.fa.* BWAindex/

STARIndex/2.4.2a/SAindex:	genome_fasta/genome.fa
	mkdir -p STARIndex/2.4.2a
	/package/STAR-2.4.2a/bin/STAR --runThreadN 10 --runMode genomeGenerate --genomeDir STARIndex/2.4.2a --genomeFastaFiles genome_fasta/genome.fa
	rm -f Log.out

STARIndex/2.7.1a/SAindex:	genome_fasta/genome.fa
	mkdir -p STARIndex/2.7.1a
	module load star/2.7.3a; STAR --runThreadN 10 --runMode genomeGenerate --genomeDir STARIndex/2.7.1a --genomeFastaFiles genome_fasta/genome.fa
	rm -f Log.out

BismarkIndex/Bisulfite_Genome/GA_conversion/BS_GA.1.bt2:	genome_fasta/genome.fa
	mkdir -p BismarkIndex
	ln -s ../genome_fasta/genome.fa BismarkIndex/genome.fa
	/package/bismark-0.16.3/bismark_genome_preparation --path_to_bowtie /package/bowtie2-2.2.3/bin BismarkIndex/

NovoalignIndex/genome:	genome_fasta/genome.fa
	mkdir -p NovoalignIndex
	ln -s ../genome_fasta/genome.fa NovoalignIndex/genome.fa
	/package/novoalign-3.07.00/novoindex NovoalignIndex/genome NovoalignIndex/genome.fa

NovoalignMethylIndex/genome:	genome_fasta/genome.fa
	mkdir -p NovoalignMethylIndex
	ln -s ../genome_fasta/genome.fa NovoalignMethylIndex/genome.fa
	/package/novoalign-3.07.00/novoindex -b NovoalignMethylIndex/genome NovoalignMethylIndex/genome.fa

#All genome aligner indices are prerequisites
GENOMEINDICES: HISAT2Index/genome.8.ht2 HISATIndex/genome.rev.2.bt2 BowtieIndex/genome.rev.2.bt2 BWAindex/genome.fa.sa STARIndex/2.4.2a/SAindex STARIndex/2.7.1a/SAindex BismarkIndex/Bisulfite_Genome/GA_conversion/BS_GA.1.bt2 NovoalignIndex/genome NovoalignMethylIndex/genome

#Attempt making the transcriptome construction parallel
$(gene_gtf_tuple)::
	$(eval PROT = $(word 1,$(subst $$, ,$@)))
	$(eval URL = $(word 2,$(subst $$, ,$@)))
	$(eval SOURCE = $(word 3,$(subst $$, ,$@)))
	$(eval VERSION = $(word 4,$(subst $$, ,$@)))
	$(eval CONV = $(word 5,$(subst $$, ,$@)))
	mkdir -p $(SOURCE)/$(VERSION)
	$(MAKE) URL=$(URL) PROT=$(PROT) CONV=$(CONV) $(SOURCE)/$(VERSION)/genes.slop.gtf
	$(MAKE) URL=$(URL) PROT=$(PROT) CONV=$(CONV) $(SOURCE)/$(VERSION)/genes.bed
	$(MAKE) URL=$(URL) PROT=$(PROT) CONV=$(CONV) $(SOURCE)/$(VERSION)/transcript2gene.txt
	$(MAKE) DIR=$(SOURCE)/$(VERSION) $(SOURCE)/$(VERSION)/tophat/tophat.rev.2.bt2
	$(MAKE) DIR=$(SOURCE)/$(VERSION) $(SOURCE)/$(VERSION)/HISAT2/splices.txt

#All transcriptome GTF/BED file and indices for alignments to them (e.g., tophat2)
#Note, these can't be run in parallel, since tophat will clash with itself
TRANSCRIPTOMES: $(gene_gtf_tuple)
