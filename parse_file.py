#!/bin/env python

import os, sys
import subprocess
from collections import defaultdict
from pprint import pprint

#============ARG PARSE=====
if len(sys.argv)>1:
    folder = sys.argv[1]
else:
    folder = os.getcwd()
if os.path.isdir(folder):
    print "BEGIN: parse file under %s" % folder
else:
    raise RuntimeError("%s is not a folder" % folder)

#============UTIL=====
def get_ftype(f):
    f_name = os.path.basename(f)
    f_l = f_name.split('.')
    if len(f_l)>1:
        if f_l[0]=='':  # .* file
            return 'dot_start'
        return f_l[-1]
    return 'normal'

def get_wc_out(f_lst):
    try:
        wc_out = subprocess.check_output(['wc', '-lc'] + f_grp)
    except Exception as e:
        print e
        return ""
    return wc_out

#============MAIN=====
result_d = defaultdict(lambda : [0, 0, 0])
file_lst = []
for root, dirs, files in os.walk(folder):
    for f in files:
        f_name = os.path.realpath(root+'/'+f)
        if os.path.isfile(f_name):
            if os.access(f_name, os.R_OK):
                file_lst.append(f_name)
            else:
                result_d["un-readable"][0] += 1
        else:
            result_d["special"][0] += 1
total_f = len(file_lst)
print "\rtotal file to parse: %d" % total_f,

step = 10000 if total_f>10000 or total_f==0 else total_f
for i in range(0, total_f, step):
    print "\rtotal file to parse: %d/%d" % (i, total_f),
    sys.stdout.flush()
    f_grp = file_lst[i:i+step]
    wc_out = get_wc_out(f_grp)
    for l in wc_out.split('\n'):
        l = l.split()
        try:
            l_cnt = int(l[0])
            b_cnt = int(l[1])
            f_name = l[-1]
        except:
            continue
        if f_name=='total':
            continue
        ft = get_ftype(f_name)
        result_d[ft][0] += 1
        result_d[ft][1] += l_cnt
        result_d[ft][2] += b_cnt
print "\rtotal file to parse: %d" % total_f

print "FILETYPE: count / line / bytecount"
for k, v in sorted(result_d.items(), key=lambda x: x[1][0]):
    print "%-10s %d\t%d\t%d" % (k, v[0], v[1], v[2])
t = reduce(lambda x,y : [x[0]+y[0], x[1]+y[1], x[2]+y[2]], result_d.values())
print "TOTAL      %d\t%d\t%d" % (t[0], t[1], t[2])

