#!/Users/datleeman/anaconda/bin/python

import oauth2 as oauth
import urllib2 as urllib

# See assignment1.html instructions or README for how to get these credentials

api_key = "UXxM4ptQwohNYgUWDVrNqlGSE"
api_secret = "f0ffMPpp81ARtp3TKvtvIlCigmO3VxowB4Op033YHODidoTuWP"
access_token_key = "16106317-syCukv6yoG8FhEIm6V3kKHB6D6Xtqt6bEIIY4WlRc"
access_token_secret = "nXhvU9flvTbgtRsVCkXU8cnRHSfumqUhuKxrfv3sRO05V"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  url = "https://stream.twitter.com/1.1/statuses/sample.json"
  '''
  Returns public statuses that match one or more filter predicates. Multiple parameters may be specified which allows most clients to use a single connection to the Streaming API. Both GET and POST requests are supported, but GET requests with too many parameters may cause the request to be rejected for excessive URL length. Use a POST request to avoid long URLs.

The track, follow, and locations fields should be considered to be combined with an OR operator. track=foo&follow=1234 returns Tweets matching "foo" OR created by user 1234.

The default access level allows up to 400 track keywords, 5,000 follow userids and 25 0.1-360 degree location boxes. If you need elevated access to the Streaming API, you should explore our partner providers of Twitter data here.
  '''
  url = "https://stream.twitter.com/1.1/statuses/filter.json?track='gay marriage'&locations=-122.75,36.8,-121.75,37.8"

  parameters = []
  response = twitterreq(url, "GET", parameters)

  for line in response:
    print line, "->", line.strip()
  print type(response)

if __name__ == '__main__':
  fetchsamples()
