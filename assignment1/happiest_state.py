#!/usr/bin/python

import json
import sys
import re
import os
import inspect
import operator

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

new_values = []
state = ""


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

def get_tweet_words(text):
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
        tweetWord =''.join(chr(c) if chr(c).isupper() \
                or chr(c).islower() else ' ' for c in range(256))
        for ignoreWord in ignoreWords:
            if ignoreWord in tweetWord:
                print tweetWord
                textArray.remove(tweetWord)
                msg = "Removing word from the list: "+ tweetWord
                output(msg,1,__function__,__file__,\
                        inspect.currentframe().f_lineno)

    msg = "Text array: " + str(textArray)
    output(msg,1,__function__,__file__,\
        inspect.currentframe().f_lineno)

    textArray = filter(None, textArray)
    
    # Convert the string to an array.
    return textArray


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
                    output(msg,8,__function__,__file__, \
                        inspect.currentframe().f_lineno)
                    scoredWords.append({'position':count, \
                                        'word':word, \
                                        'score':score, \
                                        'positive':0, \
                                        'negative':0 })
                elif score > 0:
                    word =  re.sub('\n', '', word)
                    msg = "\tFound a positionitive word: " + word \
                            + " " + scores[key]
                    output(msg,8,__function__,__file__, \
                        inspect.currentframe().f_lineno)
                    scoredWords.append({'position':count, \
                                        'word':word, \
                                        'score':score, \
                                        'positive':0, \
                                        'negative':0})
                else:
                    word =  re.sub('\n', '', word)
                    msg = "\tFound a word with zero score: " + word \
                            + " " + "0"
                    output(msg,8,__function__,__file__, \
                        inspect.currentframe().f_lineno)
                    calcWordScore.append({'word':word, \
                                        'score':score, \
                                        'positive':0, \
                                        'negative':0 })

        if found == 0:
            msg = "\tNo score found: " + word.rstrip('\n') \
               + "\t\t" + "n/a"
            output(msg,8,__function__,__file__, \
                inspect.currentframe().f_lineno)
            if key != '':
                calcWordScore.append({ 'word':word, \
                    'score':score, \
                    'positive':0, \
                    'negative':0 })

    msg = "\tTweet Sentiment Score: " + str(sumScore) + "\n"
    output(msg,5,__function__,__file__,\
        inspect.currentframe().f_lineno)
    return (sumScore)


def main():
    __function__ = 'main'

    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    data = {}
    textArray = []
    
    wordScores = readSentimentFile(sent_file)

    for line in open (tweet_file):
        encoded = unicode(line, 'utf-8')
        tweet = json.loads(encoded)
        if tweet.has_key('delete'):
            msg = "Skipping a delete object"
            output(msg,5,__function__,__file__,\
                inspect.currentframe().f_lineno)
            continue
    
        if tweet['lang'] != "en":
            msg = "Skipping a non-English tweet"
            output(msg,5,__function__,__file__,\
                inspect.currentframe().f_lineno)
            continue
    
        state = ""
        if 'place' in tweet.keys():
            if type(tweet['place']) is dict:
                place = tweet['place']
                if 'full_name' in place.keys():
                    place_name = place['full_name'].encode('ascii','ignore')
                    values = place_name.split(', ')
                    for entry in values:
                        if entry in states.keys():
                            #print "found "+str(entry)+" in state keys"
                            state = entry
                            continue
                        elif entry in states.values():
                            #print "found "+str(entry)+" in state values"
                            state = states.keys()[states.values(). \
                                    index(entry)]
                            continue
                        else:
                            msg = "\nState is: "+str(state)
                            output(msg,4,__function__,__file__,\
                                inspect.currentframe().f_lineno)
                            continue
    
        if state != '':
            text = tweet['text'].encode('ascii', 'ignore')
            # get the tweet sentiment score
            text_array = get_tweet_words (text) 

            tweet_score = get_sentiment_score(text_array, wordScores)
            
            msg = "For tweet:\n"+str(text)+"\nState is: "+str(state)+\
                    "And Sentiment Score: "+str(tweet_score)
            if tweet_score != 0:
                output(msg,1,__function__,__file__,\
                    inspect.currentframe().f_lineno)

            
            if state in data.keys():
                state_score = data.get(state) + tweet_score
                data[state] = state_score
            else:
                data[state] = tweet_score

    print max(data.iteritems(), key=operator.itemgetter(1))[0]

if __name__ == '__main__':
        main()
