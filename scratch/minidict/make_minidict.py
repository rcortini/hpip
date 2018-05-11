import pickle

# file names
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
        if items[2] != '*':
            try:
                # Use dictionary associates barcodes to promoters
                # from the library sequencing.
                promoter = bcd_promd[barcode]
                minidict[barcode] = promoter
            except KeyError:
                continue

# save to minidict file
pickle.dump(minidict, open('miniprom_bcd.p','wb'))
