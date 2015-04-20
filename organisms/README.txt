Each of the directories in this folder contains:
  * A reference genome fasta file
  * One or more reference annotation GTF files
  * A genomic index for HISAT
  * A genomic index for bowtie2
  * Transcriptome indices for tophat2 and HISAT (splices.txt).
  * Possibly additional annotations, as requested

Directories are named as AAAA_BBBB, where AAAA indicates a genome and version (e.g., GRCh38 for human version 38, or dm3 for drosophila version 3) and BBBB indicates a source and chromosome naming nomenclature (e.g., ensembl, or gencode).

The following directories will always exist and their contents will be identically names:
  * genome_fasta
    * genome.2bit (the 2bit representation of the genome)
    * genome.chrom.sizes (the length of each chromosome)
    * genome.fa (the reference fasta file)
    * genome.fa.fai (the samtools faidx)
    * genome.dict (the dictionary file, used by picard)
  * HISATIndex
    * genome.*.bt2 (the indices for HISAT)
  * BowtieIndex
    * genome.*.bt2 (the indices for bowtie2, these are actually just links to the HISAT indices since they're identical)

For each annotation source that's been requested (e.g., UCSC, gencode, Ensembl), there will exist a corresponding directory with subdirectories indicating releases (e.g., ensembl/release-78). Within each of these, the following will always exist:
  * genes.gtf (the GTF file associated with the indicated release)
  * genes.bed (a BED version of genes.gtf)
  * HISAT/splices.txt (the splice junction file for use with HISAT)
  * tophat/tophat*.bt2 (the transcriptome index for use with tophat2)
Other files may exist within these directories (e.g., repeatmasker tracks). If you would like an annotation added, please just ask. Note that coordinates and chromosome names within each of these directories will ALWAYS match the reference fasta file.

Blacklists/mappability
Note that there are blacklist files from the ENCODE project for GRCh37 and GRCm37 datasets. Likewise, there are mappability tracks using 50bp reads in bigwig format. These are all found under ENCODE/.

Examples:

Since indices for bowtie2, tophat2, and HISAT are provided, example usage of each are as follows (I assume the programs are in you $PATH):

bowtie2 -p 12 -x /data/repository/organisms/GRCm38_ensembl/BowtieIndex/genome -1 /data/my_group/fastq1.fq.gz -2 /data/my_group/fastq2.fq.gz

tophat -p 12 --transcriptome-index /data/repository/organisms/GRCm38_ensembl/ensembl/release-79/tophat/tophat /data/repository/organisms/GRCm38_ensembl/BowtieIndex/genome -1 /data/my_group/fastq1.fq.gz -2 /data/my_group/fastq2.fq.gz

hisat -p 12 --known-splicesite-infile /data/repository/organisms/GRCm38_ensembl/ensembl/release-79/HISAT/splices.txt -x /data/repository/organisms/GRCm38_ensembl/HISATIndex/genome -1 /data/my_group/fastq1.fq.gz -2 /data/my_group/fastq2.fq.gz

If you would like anything else added, please email Devon Ryan at ryan@ie-freiburg.mpg.de
