import os
from os.path import join
from pandas import read_csv, concat
from numpy import *

#------------------------------------------------------------------------------

#input data directory
dirin = join('..', 'data', 'raw')

#output data directory
dirout = join('..', 'data', 'pro')

#------------------------------------------------------------------------------

def tofile(x, d, fn):
    p = join(d, fn)
    x.tofile(p)
    print("file written:", p)

#------------------------------------------------------------------------------

#read all tables into frames and concatenate them
df = concat([read_csv(join(dirin, fn)) for fn in os.listdir(dirin)], axis=0)
#lowercase the column names
df.columns = [c.lower() for c in df.columns]
#sort by day and time
df.sort_values(by=['sol', 'timestamp'], inplace=True)
#shift the timestamp to begin at zero
df.timestamp -= df.timestamp.min()

#create a timestamp array for all slots
t = arange(0, df.timestamp.max()+1, dtype=int32)
tofile(t, dirout, "t")
#indices for mapping
idx = df.timestamp.values
#matching array for sol number
sol = full(len(t), 0, dtype=int32)
sol[idx] = df['sol'].values
tofile(sol, dirout, 'sol')
#same thing for pressure and temperature
for c in ['ambient_temp', 'pressure']:
    x = full(len(t), nan, dtype=float32)
    x[idx] = df[c].values
    tofile(x, dirout, c)