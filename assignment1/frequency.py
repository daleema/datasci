#!/usr/bin/python

__author__ = 'datleeman'
__file__   = 'term_sentiment.py'


import sys
import json
import re
import collections
import logging
import os
import inspect


def readSentimentFile(sent_file):
    __function__ = 'readSentimentFile'
    #Reads in the sentiment file.
    f = open(sent_file, 'r') # open the file for reading

    data = {}
    for row_num, line in enumerate(f):
        # Remove the new line at the end and then split the string based on
        # tabs. This creates a python list of the values.
        line   = line.strip('\n')
        values = line.split('\t')
        if row_num == 0: # first line is the header
            header = values
        else:
            data[values[0]] = values[1]

    f.close() # close the file
    return data

def get_sentiment_score(words, scores):
    __function__ = 'get_sentiment_score'
    #Pulls out the text of the tweets and prints the sum of the
    #sentiment scores for the tweet. The sum of the sentiment
    #scores is the sentiment score for the file.

    # loop over the words in the words array and look for them 
    # in the scores dict.
    sumScore = 0
    found = 0
    globalFound = 0
    score = 0
    posScore = 0
    negScore = 0
    noScore = 0
    count = 0
    scoredWords = []
    calcWordScore = []
    
    for word in words:
        found = 0
        count = count + 1

        for key in scores:
            
            if ( key == word ):
                found = 1
                globalFound = 1
                score = float(scores[key])
                sumScore = sumScore + float(scores[key])
                if score < 0:
                    word =  re.sub('\n', '', word)
                    msg = "\tFound a negative word: " + word \
                            + " " + scores[key]
                    output(msg,8,__function__,__file__)
                    scoredWords.append({'position':count, \
                                        'word':word, \
                                        'score':score, \
                                        'positive':0, \
                                        'negative':0 })
                elif score > 0:
                    word =  re.sub('\n', '', word)
                    msg = "\tFound a positionitive word: " + word \
                            + " " + scores[key]
                    output(msg,8,__function__,__file__)
                    scoredWords.append({'position':count, \
                                        'word':word, \
                                        'score':score, \
                                        'positive':0, \
                                        'negative':0})
                else:
                    word =  re.sub('\n', '', word)
                    msg = "\tFound a word with zero score: " + word \
                            + " " + "0"
                    output(msg,8,__function__,__file__)
                    calcWordScore.append({'word':word, \
                                        'score':score, \
                                        'positive':0, \
                                        'negative':0 })

        if found == 0:
            msg = "\tNo score found: " + word.rstrip('\n') \
               + "\t\t" + "n/a"
            output(msg,8,__function__,__file__)
            if key != '':
                calcWordScore.append({ 'word':word, \
                    'score':score, \
                    'positive':0, \
                    'negative':0 })

    msg = "\tTweet Sentiment Score: " + str(sumScore) + "\n"
    output(msg,4,__function__,__file__)
    return (sumScore, calcWordScore)

def additionalScoring(scoredWords):
    __function__ = 'additionalScoring'
    #print "\n\tWords with scores: "
    i = 0
    while (i <= ( len (scoredWords) - 1)):
        # If a word has been scored look at the words before and after this word.
        if ( ( scoredWords[i]['score'] != 0) and ( (i != 0) and \
                ( i != ( len(scoredWords)-1 )))):
            msg = "Found word with zero score: " + str(scoredWords[i]['word'])\
                    + "The pos is: " + str(i)
    # TODO-20140706-2013 Need to add logic to handle the case where the word
    # with zero score is the first or the last word in the list.
            previousWordIndx = i - 1
            nextWordIndx     = i + 1

            # Not sure this is what I want yet.
            if (scoredWords[previousWordIndx]['lck'] == 0):
                scoredWords[previousWordIndx]['score']= \
                        (scoredWords[i]['score']/3)
            if (scoredWords[nextWordIndx]['lck'] == 0):
                scoredWords[nextWordIndx]['score']=(scoredWords[i]['score']/3)

        i = i + 1
    return (scoredWords)

def calcTweetScore(scoredWords):
    __function__ = 'calcTweetScore'
    score = 0.0
    for word in scoredWords:
        score = score + float(word['score'])
    return score

def printEntries(list):
    __function__ = 'printEntries'
    for word in list:
        print "\n\tPosition: "+ str(word['pos']) + \
              "\tWord: "+str(word['word'])+ \
              "\tScore: "+str(word['score'])+"\n"
    return

def assignment_output(diction,count):
    __function__ = 'assignment_output'
    for key in diction.keys():
        score =  diction[key] / float(count)
        score = ("{0:.4f}".format(round(score,2)))
        print str(key)+" "+str(score)
    return

def lines(fp):
    #Prints the number of lines in the file passed in.
    print str(len(fp.readlines()))

def get_tweet_text(text):
    __function__ = 'get_tweet_text'
    out = []
    ignoreWords = [ ("rt"), ("@"), ("http"), ("#") ]

    text = re.sub('\n+', '', text)
    text = re.sub('\.+', '', text)
    text = re.sub('\:+', '', text)
    text = re.sub('\"+', '', text)
    text = re.sub('\?', '', text)
    text = re.sub('\@', '', text)
    text = re.sub('\)', '', text)

    text = ''.join(i for i in text if not i.isdigit())
    
    textArray = text.split(' ')

    for tweetWord in textArray: 
        tweetWord =''.join(chr(c) if chr(c).isupper() or chr(c).islower() else ' ' for c in range(256))
        for ignoreWord in ignoreWords:
            if ignoreWord in tweetWord:
                print tweetWord
                textArray.remove(tweetWord)
                msg = "Removing word from the list: "+ tweetWord
                output(msg,1,__function__,__file__)

    msg = "Text array: " + str(textArray)
    output(msg,1,__function__,__file__)

    textArray = filter(None, textArray)
    
    # Convert the string to an array.
    return textArray


def output(string,debuglvl,function,file):
    debug_level  = 0
    if ( os.environ.has_key('PYTHON_DEBUG') == 'True'):
        debug_level =  os.environ['PYTHON_DEBUG']

    if (debuglvl <= debug_level):
        print "DEBUG Msg from ("+function+")\n"+\
              "---------------------------------------------" + \
              "----------------------------------\n" + \
               string + "\n" +\
              "---------------------------------------------" + \
              "----------------------------------\n";

def test_output(string,debuglvl,function,file,line):
    debug_level  = 0
    if ( os.environ.has_key('PYTHON_DEBUG') == 'True'):
        debug_level =  os.environ['PYTHON_DEBUG']

    if (debuglvl <= debug_level):
        print "DEBUG Msg from ("+function+") line: ("+str(line-1)+")\n"+\
              "---------------------------------------------" + \
              "----------------------------------\n" + \
               string + "\n" +\
              "---------------------------------------------" + \
              "----------------------------------\n";

def main():
    __function__ = 'main'
    tweet_file = sys.argv[1]
    count = 0 
    wordCounts = {}

    # Get one json object from the file.
    with open(tweet_file) as f:
        for line in f:
            #print type(line)
            encoded = unicode(line, 'utf-8')
            tweet = json.loads(encoded)
            #print type(tweet)

            # If the tweet dict contains the key delete skip it
            if tweet.has_key('delete'):
                msg = "Skipping a delete object"
                test_output(msg,1,__function__,__file__, \
                        inspect.currentframe().f_lineno)
                continue
            
            count = count + 1

            text = tweet["text"].encode('ascii','ignore')
            text = re.sub('\n+', '', text)
            text = text.lower()
            
            textArray = get_tweet_text(text)

            # Build a dictionary with the word as the key 
            # and the count as the value.
            for word in textArray:

                msg = "Found a word. " + str (word)
                test_output(msg,1,__function__,__file__,inspect.currentframe().f_lineno)


                if word in wordCounts.keys():
                    msg = "Found a " + str (word)+" in "+str(wordCounts)
                    test_output(msg,1,__function__,__file__,inspect.currentframe().f_lineno)
                    wordCounts[word] += 1
                    #wordCount = wordCount + 1
                    #wordCounts[word] = wordCount
                else:
                    wordCounts[word] = 1

    assignment_output (wordCounts,count)

if __name__ == '__main__':
    main()
