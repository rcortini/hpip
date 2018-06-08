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

datadir = '/mnt/ant-login/mcorrales/HPIP/libraries'

# Lets generate a dictionary uniquely associating barcode-promoters
data_path = datadir + "/Starcoded_proms/"
fn_re = re.compile(r"Promoter[A-H][0-9][0-9]?-starcoded.txt")
starcodedfn = [fname for fname in os.listdir(data_path) if
               fn_re.match(fname)]

# library IDs: init the barcodes dictionary
lib_ids = [str(i) for i in range(1,13)]
barcodesd = dict()
for lib_id in lib_ids :
    barcodesd[lib_id] = {}

for fname in starcodedfn:
    promname = fname.split("-")[0]
    prom_lib_id = promname.split('Promoter')[1][1:]
    print "Processing %s"%(fname)
    with open(data_path + fname) as f:
        for line in f:
            bcd = line.split()[0]
            # Barcodes cannot be duplicated
            if bcd in barcodesd[prom_lib_id]:
                barcodesd[prom_lib_id][bcd].append(promname)
                continue
            barcodesd[prom_lib_id][bcd] = [promname]

# Save the dict in a pickle object using protocol 2

print "Saving output"
with open("prom_bcd_d.p", "wb") as output :
    pickle.dump(barcodesd, output, 2)
