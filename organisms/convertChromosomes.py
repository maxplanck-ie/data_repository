#!/usr/bin/env python
import csv
import argparse
import sys

def parseArguments(args=None) :
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Convert chromosome names between systems (e.g., UCSC to Ensembl). This program accepts a two column tab separated file as input. Column 1 of the file specifies the chromosome name of the input. Column 2 specifies what that name will be converted to. An empty value in column 2 indicates that any matching entries are to be ignored. Lines starting with # are ignored. Output is to stdout.")
    parser.add_argument("-n", metavar="colnum", dest="colnum", default=1, type=int, help="The column containing the chromosome name (1-based).")
    parser.add_argument('mapFile', metavar='mapFile', help="The tab-separated file containing the chromosome name mappings")
    args = parser.parse_args()
    if(args.mapFile == None) :
        parser.print_help()
        sys.exit()
    args.colnum -= 1
    return(args)

def makeMappings(fname) :
    mappings = dict()
    try: 
        for line in csv.reader(open(fname, "r"), dialect="excel-tab") :
            assert line[0] not in mappings
            if line[1] != "" :
                mappings[line[0]] = line[1]
            else :
                mappings[line[0]] = None
    except:
        sys.exit("Couldn't open %s!\n" % fname)
    return(mappings)

def main(args) :
    mappings = makeMappings(args.mapFile)
    out = sys.stdout
    lastKey = None
    lastVal = None
    for line in csv.reader(sys.stdin, delimiter="\t", quoting=csv.QUOTE_NONE) :
        if line[0].startswith("#") :
            for i in xrange(0,len(line)-1) :
                out.write("%s\t" % line[i])
            out.write("%s\n" % line[len(line)-1])
            continue

        if line[args.colnum] != lastKey:
            if line[args.colnum] not in mappings :
                sys.stderr.write("%s not in mappings!\n" % line[args.colnum])
            assert line[args.colnum] in mappings
            sys.stderr.write("%s\n" % line[args.colnum])
            lastKey = line[args.colnum]
            lastVal = mappings[line[args.colnum]]
        if(lastVal == None) :
            continue
        line[args.colnum] = lastVal

        for i in xrange(0,len(line)-1) :
            out.write("%s\t" % line[i])
        out.write("%s\n" % line[len(line)-1])

if __name__ == "__main__" :
    args = parseArguments()
    main(args)
