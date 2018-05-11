import pickle
from collections import defaultdict

# file names
# fname_bcd_dictionary = "miniprom_bcd.p" # "prom_bcd.p"
fname_bcd_dictionary = "prom_bcd.p"
fname_starcode_out = "iPCR_rep1_starcode.txt"
fname_mapped = "iPCR_rep1.sam"

# open dictionary
bcd_promd = pickle.load(open(fname_bcd_dictionary, "rb"))

# create a dictionary of "canonical" barcodes
canonical = dict()
with open(fname_starcode_out) as f:
    for line in f:
        items = line.split()
        for brcd in items[2].split(','):
            canonical[brcd] = items[0]

# counts = defaultdict(lambda: defaultdict(int))
counts = {}
ISREV = 0b10000
minidict = {}
with open(fname_mapped) as f:
    for line in f:
        if line[0] == '@':
            continue
        items = line.split()
        try:
            barcode = canonical[items[0]]
        except KeyError:
            continue
        if items[2] == '*':
            position = ('', 0)
        else:
            try:
                # Use dictionary associates barcodes to promoters
                # from the library sequencing.
                promoter = bcd_promd[barcode]
            except KeyError:
                continue
            strand = '-' if int(items[1]) & ISREV else '+'
            chrom = items[2]
            pos = int(items[3])
            ident = (chrom, pos, strand, promoter)
            if not counts.has_key(barcode) : 
                counts[barcode] = {}
            if not counts[barcode].has_key(ident) :
                counts[barcode][ident] = 0
            counts[barcode][ident] += 1

# save to minidict file
pickle.dump(counts, open('countsdict.p','wb'))
