import os
import sys
import bs4
import requests
import multiprocessing as mp

#-------------------------------------------------------------------------------
#INPUTS

#output directory
assert len(sys.argv) > 1, 'the output directory must be specified at cmd line (1st arg)'
outdir = sys.argv[1]

assert len(sys.argv) > 2, 'the number of cpus (for multiprocessing) must be specified at cmd line (2nd arg)'
cpus = int(sys.argv[2])

#rename join for creating urls/paths with single backslashes
join = lambda *args: '/'.join(args)

#base directory of data archive
baseurl = 'https://atmos.nmsu.edu/PDS/data/mslrem_1001/'

#label file url
labelurl = join(baseurl, 'LABEL', 'MODRDR6.FMT')

#top data directory url
dataurl = join(baseurl, 'DATA')

#columns to write to file
cols = ['TIMESTAMP',
        'LMST',
        'LTST',
        'AMBIENT_TEMP',
        'PRESSURE',
        'HORIZONTAL_WIND_SPEED',
        'VERTICAL_WIND_SPEED',
        'VOLUME_MIXING_RATIO',
        'LOCAL_RELATIVE_HUMIDITY']

#-------------------------------------------------------------------------------
#FUNCTIONS

#pull file from url and convert it to a string
get_file = lambda url: requests.get(url).content.decode('utf-8')

#get linked files in a single web page, from its url string
def get_links(url):
    #get html text
    html = get_file(url)
    #parse it with beautiful soup
    soup = bs4.BeautifulSoup(html, 'html.parser')
    #get path elements for all the links
    links = [link.get('href') for link in soup.find_all('a')]
    return(links)

def download(url, sol, colnums, outdir):
    #extract data
    table = get_file(url)
    #remove unwanted values
    table = table.replace('UNK','').replace('NULL','')
    #write data to new file
    with open('%s/sol_%06d.csv' % (outdir, sol), 'w') as ofile:
        #column headers
        ofile.write('SOL,' + ','.join(cols) + '\n')
        #csv body
        for line in table.strip().split('\n'):
            #split the table row on its commas
            s = line.strip().split(',')
            #select only the desired column elements
            s = [s[i].strip() for i in colnums]
            #write the elements to file, along with the sol
            ofile.write('%d,' % sol)
            ofile.write(','.join(s) + '\n')
    print('sol %s written' % sol)

#-------------------------------------------------------------------------------
#MAIN

if __name__ == '__main__':

    #make sure the output directory is there
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    #read column headers from label file
    name2num = {}
    lines = get_file(labelurl).split('\n')
    for i in range(len(lines)):
        line = lines[i]
        if('COLUMN_NUMBER' in lines[i]):
            #get the column number
            line = lines[i]
            colnum = int(line[line.index('=')+1:].strip()) - 1
            #get the column name/description from the following line
            line = lines[i+1]
            colname = line[line.index('=')+1:].strip().replace('"','')
            #save the column num and name
            name2num[colname] = colnum

    #start pool
    print('cpus = %d' % cpus)
    pool = mp.Pool(cpus)
    res = []
    #get desired column indices
    colnums = [name2num[i] for i in cols]
    #loop over all subdirectories in the data directory
    for count,dn1 in enumerate(get_links(dataurl)):
        #loop over all subdirectories in dir1
        if('SOL' in dn1):
            for dn2 in get_links(join(dataurl, dn1)):
                #loop over links in directory for single sol
                if('SOL' in dn2):
                    sol = int(dn2.replace('SOL','').replace('/',''))
                    for fn in get_links(join(dataurl, dn1, dn2)):
                        if(('RMD' in fn) and ('.TAB' in fn)):
                            url = join(dataurl, dn1, dn2, fn)
                            res.append(pool.apply_async(download,
                                    (url, sol, colnums, outdir)))
    #execute all the function calls
    [r.get() for r in res]
