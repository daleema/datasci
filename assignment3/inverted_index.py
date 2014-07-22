#!/usr/bin/python

__author__ = 'datleeman'
__file__   = 'inverted_index.py'

import sys
import json
import re
import os
import inspect
import MapReduce

mr = MapReduce.MapReduce()

def output(string,debuglvl,function,file,line):
    debug_level  = 0
    if ( os.environ.has_key('PYTHON_DEBUG') == 'True'):
        debug_level =  os.environ['PYTHON_DEBUG']

    if (debuglvl <= debug_level):
        print "DEBUG Msg from ("+function+") line: ("+str(line-2)+")\n"+\
              "---------------------------------------------" + \
              "----------------------------------\n" + \
               string + "\n" +\
              "---------------------------------------------" + \
              "----------------------------------\n";
# Use msg = "Skipping a delete object"
# test_output(msg,1,__function__,__file__,inspect.currentframe().f_lineno)


def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      if w == '[':
        continue
      w = w.encode('ascii','ignore')
      key = key.encode('ascii','ignore')
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word 
    # value: list of documents
    dict = {}
    dict[key] = list_of_values

    #print str(key) + " "+ str(list_of_values)
    print str(dict) 

def main():
    __function__ = 'main'
    inputdata = open(sys.argv[1])
    msg = "Imput data "+str(inputdata)
    output(msg,1,__function__,__file__,inspect.currentframe().f_lineno)
    mr.execute(inputdata, mapper, reducer)

if __name__ == '__main__':
    main()
