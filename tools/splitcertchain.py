#!/usr/bin/python3

import os
import sys

def fatal (msg):
    print ("ERROR:%s" % msg)
    sys.exit(-1)

def debug (msg):
    global debugctl
    if debugctl:
        print ("DEBUG:%s" % msg)

def newofn ():
    global i
    fn = "cert_" + str(i) + ".cer"
    debug ("i=%d fn=%s" % (i, fn))
    i += 1
    return fn
 
# --- main ---

BEGIN = 0
B64 = 1
B64OREND = 2

if len(sys.argv) != 2:
    fatal ("missing input filename")

debugctl = False
debugctl = True
i = 0
ofn = newofn()

inf = sys.argv[1]
debug ("inf=%s" % inf)

allcerts = (open(inf, "r")).readlines()
fh = None
expect = BEGIN

for cl in allcerts:
    cl = cl.strip()
    debug (".%s" % cl)
    if "--BEGIN" in cl:
        if expect != BEGIN:
            fatal ("malformed input file 0")
        expect = B64
        debug ("opening file=%s" % ofn)
        fh = open(ofn, "w")
        fh.write ("%s\n" % cl)
        continue
    if "--END" in cl:
        if expect != B64OREND:
            fatal ("malformed input file 1")
        expect = BEGIN
        debug ("closing file=%s" % ofn)
        fh.write ("%s\n" % cl)
        fh.close ()
        fh = None
        ofn = newofn()
        continue
    if (expect == B64) or (expect == B64OREND):
        expect = B64OREND
        fh.write ("%s\n" % cl)
        continue
    fatal ("malformed input file 2")

if expect != BEGIN:
    fatal ("malformed input file 3")

print ("OK")
sys.exit (0)
