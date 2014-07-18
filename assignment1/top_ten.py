#!/usr/bin/python

import json
import sys
import os
import inspect
import operator

def output(string,debuglvl,function,file,line):
    debug_level  = 0
    if ( os.environ.has_key('PYTHON_DEBUG') == 'True'):
        debug_level =  os.environ['PYTHON_DEBUG']

    if (debuglvl <= debug_level):
        print "DEBUG Msg from ("+function+") line: ("+str(line)+")\n"+\
              "---------------------------------------------" + \
              "----------------------------------\n" + \
               string + "\n" +\
              "---------------------------------------------" + \
              "----------------------------------\n";

def main():
    __function__ = 'main'

    tweet_file = sys.argv[1]

    new_values = []
    hash_tags = {}
    
    for line in open (tweet_file):
        encoded = unicode(line, 'utf-8')
        tweet = json.loads(encoded)
        if tweet.has_key('delete'):
            continue
    
#        if tweet['lang'] != "en":
#            msg = "Skipping a non-English tweet"
#            output(msg,5,__function__,__file__, \
#                    inspect.currentframe().f_lineno)
#            continue
    
        if 'entities' in tweet.keys():
            if type(tweet['entities']) is dict:
                entities = tweet['entities']
                hashtags = entities['hashtags']
                text     = tweet['text'].encode('ascii', 'ignore')
                msg = "Tweet Text:i\n"+str(text)
                output(msg,5,__function__,__file__, \
                    inspect.currentframe().f_lineno)
                for tag in hashtags:
                    my_hash_tag = tag['text']

                    if my_hash_tag in hash_tags.keys():
                        my_hash_tag_score = hash_tags.get(my_hash_tag)\
                            + 1 
                        hash_tags[my_hash_tag] = my_hash_tag_score
                    else:
                        hash_tags[my_hash_tag] = 1
    
    sorted_tags = sorted(hash_tags.iteritems(), key=operator.itemgetter(-1))
    length = len(sorted_tags) - 1
    counter = length - 9
    while counter <= length:
        print sorted_tags[counter][0] + " " + str(sorted_tags[counter][1])
        counter = counter + 1

if __name__ == '__main__':
        main()
