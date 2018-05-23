#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pickle
import sys
import re
import subprocess
from collections import defaultdict

# Enter library sequencing directories and extract
# the barcodes of each Promoter to starcode them.

SUBDIR = '/Data/Intensities/BaseCalls/'
prefix = re.compile(r'HPIP_bcds_*')
seq_dirs = [os.path.abspath(seqd) for seqd in os.listdir(".")
            if os.path.isdir(seqd) and prefix.match(seqd)]

for sdir in seq_dirs:
    data_path = sdir + SUBDIR
    fn_re = re.compile(r'Promoter[A-H][0-9][0-9]?.fastq')
    prom_fnames = [fname for fname in os.listdir(data_path)
                   if fn_re.match(fname)]

    # Extract the barcodes of each promoter file
    for fname in prom_fnames:
        prom_name = fname.split('.')[0]
        outfname = data_path + prom_name + '_to_starcode.txt'
        # Check if file was already processed
        if os.path.isfile(outfname):
            sys.stdout.write("Sample: %s already processed, skiping.\n"
                             % outfname.split('/')[-1])
            continue

        sys.stdout.write("Processing sample: %s\n" % prom_name)
        with open(data_path + fname) as f, open(outfname, 'w') as g:

            for lineno, line in enumerate(f):
                # Take sequence only.
                if lineno % 4 != 1:
                    continue
                g.write("%s\n" % line[:20])

    # Starcode each Promoter barcode file and put the result
    # in a Directory: ./Starcoded_proms
    fn_re = re.compile(r"Promoter[A-H][0-9][0-9]?_to_starcode.txt")
    starcodefn = [fname for fname in os.listdir(data_path) if
                  fn_re.match(fname)]

    outdir = os.getcwd() + "/Starcoded_proms/"
    for stc_fname in starcodefn:
        outfname = outdir + (stc_fname.split('_')[0] + '_starcoded.txt')
        # Check if file was already processed
        if os.path.isfile(outfname):
            sys.stdout.write("Sample: %s already processed, skiping.\n"
                             % outfname.split('/')[-1])
            continue

        sys.stdout.write("Starcoding sample: %s\n" % stc_fname)
        with open(outfname, 'w') as f:
            p = subprocess.Popen([
                'starcode',
                '-t1',
                '-d2',
                '--print-clusters',
                '-i',
                data_path + stc_fname],
                stdout=f)

# Lets generate a dictionary uniquely associating barcode-promoters
data_path = os.getcwd() + "/Starcoded_proms/"
fn_re = re.compile(r"Promoter[A-H][0-9][0-9]?_starcoded.txt")
starcodedfn = [fname for fname in os.listdir(data_path) if
               fn_re.match(fname)]

barcodesd = dict()

for fname in starcodedfn:
    with open(data_path + fname) as f:
        promname = fname.split("_")[0]
        for line in f:
            bcd = line.split()[0]
            # Barcodes cannot be duplicated
            if bcd in barcodesd:
                barcodesd[bcd] = 'Colision'
                continue
            barcodesd[bcd] = promname

# Save the dict in a pickle object using protocol 2

output = open("prom_bcd.p", "wb")
pickle.dump(barcodesd, output, 2)
output.close()
