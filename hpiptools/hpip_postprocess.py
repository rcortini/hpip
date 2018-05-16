import numpy as np
import hpiptools as ht
import sys

def filter_and_name_insertion(insertion,
                          chromosome_list=['2L','2R','3L','3R','4','X','Y']) :
    p = insertion['promoter']
    if p == 'Colision' :
        return None
    else :
        if insertion['chr'] not in chromosome_list :
            return None
        else :
            insertion['promoter'] = ht.plate_to_prom[p]
            return insertion


def normalize_expression(insertion) :
    if insertion['gDNA']==0 :
        # TODO: decide what to do here
        return None
    else :
        return insertion['mRNA']/float(insertion['gDNA'])

# check for proper invocation
if len(sys.argv) < 2:
    print "Usage: python hpip_postprocess.py <production_dir>"
    sys.exit(1)

# GET
production_dir = sys.argv[1]
reps = []
for rep_name in ['rep1','rep2'] :
    rep_fname = '%s/%s/HPIP_iPCR_%s_insertions.txt'%(production_dir,rep_name,rep_name)
    rep = ht.load_hpip_results(rep_fname,rep_name)
    reps.append(rep)
    
# MERGE
merged = np.concatenate([r for r in reps])
del reps

# SORT
merged.sort(order=['chr','coord'])

# FILTER AND NAME
filtered = []
for insertion in merged :
    f = filter_and_name_insertion(insertion)
    if f is not None :
        filtered.append(f)
filtered = np.array(filtered)        
# no need of storing the intermediate structure
del merged

# NORMALIZE
normalized_dtype = [
    ('barcode','S32'),
    ('chr','S4'),
    ('coord',np.int32),
    ('strand','S2'),
    ('promoter',np.int32),
    ('rep','S8'),
    ('expression',float)
]
normalized = np.zeros(filtered.size,dtype=np.dtype(normalized_dtype))
keep = ['barcode','chr','coord','strand','promoter','rep']
for i,insertion in enumerate(filtered) :
    for param in keep :
        normalized[i][param] = insertion[param]
    n = normalize_expression(insertion)
    if n is None :
        n = -100
    normalized[i]['expression'] = n
del filtered

# WRITE RESULTS

# a plain, democratic text file
out_fname = '%s/HPIP_results.txt'%(production_dir)
with open(out_fname, 'w') as f :
    f.write('# barcode chromosome strand coordinate promoter replicate expression\n')
    for insertion in normalized :
        f.write('%s\t%s\t%s\t%d\t%s\t%s\t%f\n'%(
            insertion['barcode'],
            insertion['chr'],
            insertion['strand'],
            insertion['coord'],
            insertion['promoter'],
            insertion['rep'],
            insertion['expression']
        ))

# and a npy file for the Python enthusiasts
out_fname = '%s/HPIP_results.npy'%(production_dir)
np.save(out_fname,normalized)
