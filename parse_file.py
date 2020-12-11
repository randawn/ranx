#!/bin/env python

import os, sys
import subprocess
from collections import defaultdict
from pprint import pprint

if len(sys.argv)>1:
    folder = sys.argv[1]
else:
    folder = os.getcwd()

def get_ftype(f):
    f_l = f.split('.')
    if len(f_l)>1:
        if f_l[0]=='':  # .* file
            return 'dot_start'
        return f_l[-1]
    return 'normal'

result_d = defaultdict(lambda : [0, 0, 0])
for root, dirs, files in os.walk(folder):
    for f in files:
        f_name = root+'/'+f
        ft = get_ftype(f)
        fl = int(subprocess.check_output(['wc', '-l', f_name]).split()[0])
        fs = os.stat(f_name).st_size
        result_d[ft][0] += 1
        result_d[ft][1] += fl
        result_d[ft][2] += fs

print "FILETYPE: count / line / bytecount"
for k, v in result_d.items():
    print "%-10s %d\t%d\t%d" % (k, v[0], v[1], v[2])
t = reduce(lambda x,y : [x[0]+y[0], x[1]+y[1], x[2]+y[2]], result_d.values())
print "TOTAL      %d\t%d\t%d" % (t[0], t[1], t[2])


