import numpy as np

def load_hpip_results(fname) :
    """
    Loads the results of a HPIP experiment replicate into a data structure that
    contains all the information, accessible via a numpy array.
    """
    hpip_dtype = [
        ('barcode','S32'),
        ('chr','S32'),
        ('strand','S2'),
        ('coord',np.int32),
        ('mRNA',np.int32),
        ('promoter','S32'),
        ('cDNA',np.int32),
        ('gDNA',np.int32)
    ]
    return np.genfromtxt(fname, dtype=np.dtype(hpip_dtype))


class HPIPReplicate :
    """
    A class to contain conveniently the information on an HPIP experiment
    """
    def __init__(self,name,
                 hpip_root_dir = '%s/work/CRG/projects/hpip'%(os.getenv('HOME'))) :
        self.name = name
        production_dir = '%s/production'%(hpip_root_dir)
        fname = '%s/%s/HPIP_iPCR_%s_insertions.txt'%(production_dir,name,name)
        if os.path.exists(rep_fname) :
            self.data = load_hpip_results(fname)

class HPIPMatrix :
    def __init__(self,dtype=np.int32) :
        # first, define the rows and columns of the matrix
        self.rows = ['A','B','C','D','E','F','G','H']
        self.columns = range(1,13)
        # create the names of each element of the matrix
        self.libraries = ['Promoter%s%d'%(l,n)
                    for l in self.rows
                    for n in self.columns]
        # define the matrix of elements M and the matrix of collisions C
        self.M = np.zeros((len(self.rows),len(self.columns)),dtype=dtype)
        self.C = np.zeros(1,dtype=dtype)
        # internal lightweight dictionary to map names of promoters to matrix
        # elements
        self._prom_to_idx = {}
        for i,row in enumerate(self.rows) :
            for j,column in enumerate(self.columns) :
                self._prom_to_idx['Promoter%s%d'%(row,column)] = (i,j)
    def map_name_to_idx(self,name) :
        return self._prom_to_idx[name]
    def __getitem__(self,name) :
        if name == 'Colision' :
            return self.C
        try :
            return self.M[self.map_name_to_idx(name)]
        except KeyError :
            print "Error: %s does not exist"%(name)
    def __setitem__(self,name,val) :
        if name == 'Colision' :
            self.C = val
        else :
            try :
                self.M[self.map_name_to_idx(name)] = val
            except KeyError :
                print "Error: %s does not exist"%(name)
