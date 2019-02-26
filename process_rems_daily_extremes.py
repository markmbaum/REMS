import os
import sys
import pandas as pd
import multiprocessing as mp

#-------------------------------------------------------------------------------
#INPUT

#output directory
assert len(sys.argv) > 1, 'the data directory must be specified at cmd line (1st arg)'
datadir = sys.argv[1]

#output directory
assert len(sys.argv) > 2, 'the output file name must be specified at cmd line (2nd arg)'
fnout = sys.argv[2]

assert len(sys.argv) > 3, 'the number of cpus (for multiprocessing) must be specified at cmd line (3rd arg)'
cpus = int(sys.argv[3])

#variables/columns to include in the processed file
cols = ['AMBIENT_TEMP',
        'PRESSURE',
        'HORIZONTAL_WIND_SPEED',
        'VERTICAL_WIND_SPEED',
        'VOLUME_MIXING_RATIO',
        'LOCAL_RELATIVE_HUMIDITY']

#-------------------------------------------------------------------------------
#FUNCTIONS

def process_csv(fn, cols, rows):
    #load csv
    df = pd.read_csv(fn, error_bad_lines=False)
    sol = df.at[0,'SOL']
    #write sol number
    row = str(int(sol))
    #write min and max of each column
    for c in cols:
        row += (',%g,%g' % (df[c].min(), df[c].max()))
    rows.append(row + '\n')
    print('file processed:', fn)
    del(df)

#-------------------------------------------------------------------------------
#MAIN

if __name__ == '__main__':

    #get file names
    fns = [os.path.join(datadir, fn) for fn in os.listdir(datadir)]
    fns = [fn for fn in fns if (fn[-4:] == '.csv')]
    fns = fns[:]

    #run through data for each sol, writing min and max of each col to file
    print('cpus: %d' % cpus)
    man = mp.Manager()
    rows = man.list()
    p = mp.Pool(cpus)
    args = zip(fns, [cols]*len(fns), [rows]*len(fns))
    p.starmap(process_csv, args)

    #write file, sorted by sol
    with open(fnout, 'w') as ofile:
        ofile.write('SOL')
        for c in cols:
            ofile.write(',%s_min,%s_max' % (c,c))
        ofile.write('\n')
        for row in sorted(rows, key=lambda r: int(r.split(',')[0])):
            ofile.write(row.replace('nan',''))
    print('processed data written to:', fnout)
