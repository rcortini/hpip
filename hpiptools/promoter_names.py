# first, define the rows and columns of the matrix
plate_rows = ['A','B','C','D','E','F','G','H']
plate_columns = range(1,13)
nclasses = 10

# create the names of each element of the matrix
plate_names = ['Promoter%s%d'%(l,n)
               for l in plate_rows
               for n in plate_columns]

plate_to_prom = {}
prom_to_plate = {}
for i,plate_row in enumerate(plate_rows) :
    for j,plate_column in enumerate(plate_columns) :
        plate_name = 'Promoter%s%d'%(plate_row,plate_column)
        prom_name = nclasses*i + j + 1
        plate_to_prom[plate_name] = prom_name
        prom_to_plate[prom_name] = plate_name
