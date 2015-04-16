#!/usr/bin/env python
import csv
import argparse
import sys

def parseArguments(args=None) :
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                    description="Given BED input via a pipe, append to it one record for each missing contig/chromosome. This is most useful for blacklist BED files from Encode, where patch and alternate haplotype contigs may not be included in the BED file. This will also add mitochondria (MT or chrM, as appropriate).")
    parser.add_argument(dest = 'fai', metavar="genome.fa.fai", default=None, help="The genome index file produced by samtools faidx (i.e., genome.fa.fai).")
    args = parser.parse_args()
    if(args.fai == None) :
        parser.print_help()
        sys.exit()
    return(args)

def parseFai(fname) :
    contigs = dict()
    try :
        for line in csv.reader(open(fname, "r"), dialect="excel-tab") :
            contigs[line[0]] = line[1]
    except :
        sys.exit("Couldn't open %s!\n" % fname)
    return contigs

def main(args) :
    contigs = parseFai(args.fai)
    out = sys.stdout
    ncols = 3
    for line in csv.reader(sys.stdin, delimiter="\t", quoting=csv.QUOTE_NONE) :
        if line[0].startswith("#") :
            for i in xrange(0,len(line)-1) :
                out.write("%s\t" % line[i])
            out.write("%s\n" % line[len(line)-1])
            continue

        #Remove the contig from the hash table
        if line[0] in contigs :
            del contigs[line[0]]

        if len(line) > ncols :
            ncols = len(line)

        #write the original line
        for i in xrange(0,len(line)-1) :
            out.write("%s\t" % line[i])
        out.write("%s\n" % line[len(line)-1])

    #Write out any keys remaining in the dict
    for k, v in contigs.iteritems() :
        out.write("%s\t%s\t%s" % (k, 0, v))
        if(ncols >= 4) :
            out.write("\t.")
        if(ncols >= 5) :
            out.write("\t1000")
        if(ncols >= 6) :
            out.write("\t+")
        if(ncols >= 7) :
            out.write("\t0")
        if(ncols >= 8) :
            out.write("\t%s" % v)
        if(ncols >= 9) :
            out.write("\t255,255,0") #Arbitrary!
        if(ncols >= 10) :
            out.write("\t1")
        if(ncols >= 11) :
            out.write("\t%s" % v)
        if(ncols >= 12) :
            out.write("\t0")
        out.write("\n")

if __name__ == "__main__" :
    args = parseArguments()
    main(args)
