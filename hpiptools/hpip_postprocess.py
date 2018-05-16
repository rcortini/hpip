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

def normalize_insertions(insertions) :
    # we first get the sum of all the reads of mRNA and gDNA, per replicate
    reps = np.unique(insertions['rep'])
    mRNA_sum = {}
    gDNA_sum = {}
    for rep in reps :
        # get replicate-specific insertions
        rep_mask = insertions['rep']==rep
        # get sum of mRNA, sum of gDNA, and average mRNA of the replicate
        mRNA_sum[rep] = insertions[rep_mask]['mRNA'].sum()
        gDNA_sum[rep] = insertions[rep_mask]['gDNA'].sum()
    # then we initialize the "normalized" array, and fill it with the stuff
    # that was already contained in the passed array
    normalized_dtype = [
        ('barcode','S32'),
        ('chr','S4'),
        ('coord',np.int32),
        ('strand','S2'),
        ('promoter',np.int32),
        ('rep','S8'),
        ('expression',float)
    ]
    normalized = np.zeros(insertions.size,dtype=np.dtype(normalized_dtype))
    keep = ['barcode','chr','coord','strand','promoter','rep']
    for param in keep :
        normalized[param] = insertions[param]
    # finally, we normalize the expression
    nan_mask = insertions['gDNA'] == 0
    # insertions with zero gDNA counts have NAN expression
    expression = np.zeros(insertions.size)
    expression[nan_mask] = np.nan
    # the others, we do log(eps/<eps>), specific for each replicate, where
    # eps = (mRNA/mRNA_sum)/(gDNA/gDNA_sum)
    for rep in reps :
        rep_mask = insertions['rep']==rep
        mask = np.logical_and(~nan_mask,rep_mask)
        eps = (insertions[mask]['mRNA']/float(mRNA_sum[rep]))/\
              (insertions[mask]['gDNA']/float(gDNA_sum[rep]))
        eps_mean = eps.mean()
        expression[mask] = np.log2(eps/eps_mean)
    normalized['expression'] = expression
    return normalized

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
normalized = normalize_insertions(filtered)

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
