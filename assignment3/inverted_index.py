#!/usr/bin/python
'''
output should be a list of list. 
Output is not a string  but a list of list: First element of the list is the word and the next element is the list of docids.
Docids have to be unique. You can compare the output file with solutions/inverted_index.json... It matches exactly.
Getting unique ids is simple . use set(list) and convert it back to the list using list()
'''

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
               str(string) + "\n" + \
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
      w = w.encode('ascii','ignore')
      key = key.encode('ascii','ignore')
      mr.emit_intermediate(str(w), str(key))

def reducer(key, list_of_values):
    # key: word 
    # value: list of documents
    msg = "Key is: "+str(key)+"\n"+"List of values: "+str(list_of_values)
    #output(msg,1,reducer,__file__,inspect.currentframe().f_lineno)
    docs = []
    for item in list_of_values:
        if item in docs:
            continue
        docs.append(item)
    mr.emit((key, docs))


def main():
    __function__ = 'main'
    inputdata = open(sys.argv[1])
    msg = "Imput data "+str(inputdata)
    output(msg,1,__function__,__file__,inspect.currentframe().f_lineno)
    mr.execute(inputdata, mapper, reducer)

if __name__ == '__main__':
    main()
