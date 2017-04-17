## Your name:Ankita Avadhani
## The option you've chosen: Option 2

# Put import statements you expect to need here!
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
__version___ = "0.1"
import json
import sqlite3
import re
import requests
import json
import sys
import urllib

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


CACHE_FNAME = "twitter_data.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


CACHE_FNAME = "movie_data.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


############################ Json for OMDB ################
try:
	from urllib.parse import quote
except:
	from urllib import quote
try:
	from urllib.request import urlopen
except:
	from urllib2 import urlopen
################################################################# Twitter Data Extraction ######################################
class TwitterHandler:
	
	def __init__(self, consumer_key, consumer_key_secret, access_token, 
		access_token_secret):
		self.consumer_key = consumer_key		
		self.consumer_key_secret = consumer_key_secret
		self.access_token = access_token
		self.access_token_secret = access_token_secret
		self.tweets = []


	def search(self, keyword):
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_key_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		api = tweepy.API(auth)

		tweets = api.search(q=keyword, result_type="popular", count=4, 
			include_entities=False, lang="en")
		self.tweets = sorted(tweets, key=lambda x : x.favorite_count, reverse=True)[0:5]

		return self


	def display_results(self):
		for tweet in self.tweets:
			print (tweet.text) 
			print ("Favorites: " + str(tweet.favorite_count))
			print ("Author:    " + tweet.author.name)
			print ("Time:      " + str(tweet.created_at))
			print ("---")


	def get_results(self):
		return self.tweets
###################################################################### OMDB Movies Class ##################################################
'''class Movies:
    # Class constructor.
    def __init__ (self):
        self.urlApi = "http://www.omdbapi.com"
        self.results = []
        self.numItems = -

    # Find a film using a title as a parameter
    def findFilmByTitle (self, title):
        self.title = title

        # Read the content of the url.
        searchUrl = self.urlApi + "/?s=" + self.title

        content = urlopen (searchUrl)
        jsonData = content.readall().decode('utf-8')
        content.close()

        # Parse the string as json.
        self.results = json.loads (jsonData)

        if "Response" in self.results :
            self.numItems = 0
        else:
            self.numItems = len (self.results["Search"])

    def findFilmById (self, imdbId):
        # Imdb identifier.
        self.imdbId = imdbId

        # Build the url.
        searchUrl = self.urlApi + "/?i=" + self.imdbId + "&plot=full&r=json"

        # Open url as a file.
        content = urlopen (searchUrl)
        jsonData = content.readall().decode('utf-8')
        content.close()

        # Parse the string as json
        self.ids = json.loads(jsonData)

    # Get results of a query.
    def getResults (self):
        if "Response" in self.results :
            return -1
        else:
            return self.results["Search"]

    # Get the entries number of query.
    def getNumItems (self):
        return self.numItems

    # Get all the information about one film.
    def getFilm (self):
        return self.ids
     '''


def check_if_required_key_entered(var, var_alias_name, print_text):
	if(len(var) == 0):
		print ("{0} field is required!").format(var_alias_name)
		var = input(print_text)
		check_if_required_key_entered(var, var_alias_name, print_text)
	else:
		pass

def search():
	# get item type to be searched
	item_type = input("Type (movie/series/episode) : ")
	check_if_required_key_entered(item_type, 'Type', 'Type (movie/series/episode) : ')

	if(item_type.lower() == "episode" or item_type.lower() == "series"):
		# get item title
		title = input("Series Title : ")
		check_if_required_key_entered(title, 'Title', 'Series Title : ')
		title = urllib.parse.urlencode({'': title})[1:]

		# get season and episode number
		if(item_type.lower() == "episode"):
			season = input("Season : ")
			check_if_required_key_entered(season, 'Season', 'Season : ')

			episode = input("Episode number : ")
			check_if_required_key_entered(episode, 'Episode', 'Episode number : ')

	else:
		# get item title
		title = input("Movie Title : ")
		check_if_required_key_entered(title, 'Title', 'Movie Title : ')
		title = urllib.parse.urlencode({'': title})[1:]

	# base url
	url = 'http://www.omdbapi.com/?tomatoes=true&plot=full&'

	# add search parameters
	url += 't=' + title + '&'

	url += 'type=' + item_type + '&'

	if(item_type == 'episode'):
		url += 'season=' + season + '&' + 'episode=' + episode

	# print url

	response = urllib.request.urlopen(url)
	resp_text = urllib.request.urlopen(url).read().decode('UTF-8')
	url_data = json.loads(resp_text)

	outputArray = ['Title', 'Year', 'Released', 'Runtime', 'Country', 'Language', 'Genre', 'Director', 'Writer', 'Actors', 'Awards', 'Actors', 'imdbRating', 'imdbVotes', 'Plot']
	url_data_keys = url_data.keys()

	if(url_data['Response'] == 'True'):
		print ('\n')
		print ('-------------**************-------------')
		print ('\n')

		for item in outputArray:

			if(item in url_data_keys and url_data[item] != 'N/A'):
				if(item == 'imdbVotes'):
					print ('IMDB Votes:')
				elif(item == 'imdbRating'):
					print ('IMDB Rating:')
				else:
					print (item + ':')
				print (url_data[item].encode('utf-8'))
				print ('\n')

		print ('-------------**************-------------')
		print ('\n')

	else:
		print ('Error fetching data')
		print ('\n')

	search_again = input('Wanna search again? (y/n): ')

	if(search_again.lower() == 'y' or search_again.lower() == 'yes'):
		print ('\n')
		search()
	else:
		pass
search()

def main():
	print("This program will return the five top favorited tweets that "
		"contain the movie term and all the OMDB data that had "
		"the movie term in its tags\n")
	keyword =input("Enter a Movie Title: ")


	print("\nTwitter Results:\n")
	TwitterHandler(consumer_key="2Ymp2it5w0Fo6NLYtCks6us6J", 
		consumer_key_secret="nR8sLcpMkhCzRMdk3quj8WIHZ8GN3mgAMExa7FZC4f0pmWGZLE",
		access_token="2794460791-8vBk2E9cALfIcNreZi8qcPKvnqBk09DVQzjSCEC",
		access_token_secret="kblC44rTKKOd79MeTMDxNzoceQJglVRjNv1DNGN67g9kf")\
		.search(keyword).display_results()
	
	def get_five_tweets(search):
		tweet_identity = "twitter_{}".format(search)
		if tweet_identity in CACHE_DICTION:
			content = CACHE_DICTION[tweet_identity]
		else:
			api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
			data = api.search(q=search)
			content = data["statuses"]
			CACHE_DICTION[tweet_identity] =content
			twitter_f = open(CACHE_FNAME, "w")
			twitter_f.write(json.dumps(CACHE_DICTION))
			twitter_f.close()
		five_tweets_phrases = []
		for tweet in content[:5]:
			five_tweets_phrases.append(tweet["text"])
		return(five_tweets_phrases)
	movie_tweets = get_five_tweets("Movies")

main()

######################################################### Loading Twitter data into SQL Database ###########################





	























