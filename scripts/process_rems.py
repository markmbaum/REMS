import os
from os.path import join
from pandas import read_csv, concat
from numpy import *
import multiprocessing as mp

#------------------------------------------------------------------------------

#input data directory
dirin = join('..', 'data', 'raw')

#output data directory
dirout = join('..', 'data', 'pro')

#number of processes to read data with
nproc = 6

#------------------------------------------------------------------------------

def tofile(x, d, fn):
    p = join(d, fn + '_' + str(x.dtype))
    x.tofile(p)
    print("file written:", p)

#------------------------------------------------------------------------------

if __name__ == "__main__":

    #read all tables into frames
    fns = [fn for fn in os.listdir(dirin) if fn[-4:] == '.csv']
    print('reading {0} files with {1} processes'.format(len(fns), nproc))
    pool = mp.Pool(nproc)
    tasks = [pool.apply_async(read_csv, (join(dirin, fn),)) for fn in fns]
    dfs = [task.get() for task in tasks]

    #combine all the frames
    df = concat(dfs, axis=0)
    #lowercase the column names
    df.columns = [c.lower() for c in df.columns]
    #sort by day and time
    df.sort_values(by=['sol', 'timestamp'], inplace=True)
    #shift the timestamp to begin at zero
    df.timestamp -= df.timestamp.min()
    #replace the index
    df.index = range(len(df))
    #use more efficient data types
    df.sol = df.sol.astype(int32)
    for c in df.columns[2:]:
        df[c] = df[c].astype(float32)
    #write to feather
    df.to_feather(join(dirout, 'rems.feather'))
