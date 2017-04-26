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
import omdb
__version___ = "0.1"
#### Setting up twitter key:
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)



### Caching the movie data:
MOVIE_CACHE_FNAME = "omdb_data.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	MOVIE_CACHE_DICTION = json.loads(cache_contents)
except:
	MOVIE_CACHE_DICTION = {}

### Caching the twitter data:
TWITTER_CACHE_FNAME = "twitter_data.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	TWITTER_CACHE_DICTION = json.loads(cache_contents)
except:
	TWITTER_CACHE_DICTION = {}

##Setting up the json 

############################ Json for OMDB ################
try:
	from urllib.parse import quote
except:
	from urllib import quote
try:
	from urllib.request import urlopen
except:
	from urllib2 import urlopen
#################################################### Caching Functions ##########################

#Setting up for cache function for tweets:
def cache_top_tweets(search):
		tweet_identity = "twitter_{}".format(search)
		if tweet_identity in TWITTER_CACHE_DICTION:
			content = TWITTER_CACHE_DICTION[tweet_identity]
			print('used cached data for', tweet_identity)
		else:
			print('retrieving tweets for', tweet_identity)
			api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
			data = api.search(q=search)
			content = data["statuses"]
			TWITTER_CACHE_DICTION[tweet_identity] =content
			twitter_f = open(TWITTER_CACHE_FNAME, "w")
			twitter_f.write(json.dumps(TWITTER_CACHE_DICTION))
			twitter_f.close()
		five_tweets_phrases = []
		for tweet in content:
			five_tweets_phrases.append(tweet["text"])
		return(five_tweets_phrases)

#Setting up cache function omdb data:
def get_omdb_data(movie_title):
	if movie_title in MOVIE_CACHE_DICTION:
		print('using cached data for', movie_title)
		movie_info = MOVIE_CACHE_DICTION[movie_title]
	else:
		print('getting omdb movie data for', movie_title)
		movie_info = omdb.title(movie_title)
		MOVIE_CACHE_DICTION[movie_title] = movie_info
		f= open(MOVIE_CACHE_FNAME, 'w')
		f.write(json.dumps(MOVIE_CACHE_DICTION))
		f.close()
	return movie_info

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


	def get_results(self):
		return self.tweets
###################################################################### OMDB Movies Class ##################################################
class Movies:
    # Class constructor.
    def __init__ (self,data):
        self.urlApi = "http://www.omdbapi.com"
        self.results = []
        self.numItems = 0


    # Find a film using a title as a parameter
    def findFilmByTitle (self, title):
        self.title = title

        # Read the content of the url.
        searchUrl = self.urlApi + "/?s=" + self.title

        content = urlopen(searchUrl)
        jsonData = content.readall().decode('utf-8')
        content.close()

        # Parse the string as json.
        self.results = json.loads(jsonData)

        if "Response" in self.results :
            self.numItems = 0
        else:
            self.numItems = len(self.results["Search"])

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
        self.ids = json.loads (jsonData)

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


    def get_actors(self, num_actors = 1):
    	actors_returned = []
    	for index, actor in enumerate(self.actors):
    		if index == num_actors:
    		 break
    		 actors_returned.append(actor)
    	return actors_returned

    




################################################################ Invoking and Displaying Results ###################################################
def main():
	print("This program will retrieve twitter data and omdb data on three movies selected \n")
	movies=[ "Logan", "Captain America", "Finding Dory"]
	
	print("\nTwitter Results:\n")
	TwitterHandler(consumer_key="2Ymp2it5w0Fo6NLYtCks6us6J", 
		consumer_key_secret="nR8sLcpMkhCzRMdk3quj8WIHZ8GN3mgAMExa7FZC4f0pmWGZLE",
		access_token="2794460791-8vBk2E9cALfIcNreZi8qcPKvnqBk09DVQzjSCEC",
		access_token_secret="kblC44rTKKOd79MeTMDxNzoceQJglVRjNv1DNGN67g9kf")\
		.search("Movies")
main()
	
movie_tweets = cache_top_tweets("Logan")
movie_tweets=cache_top_tweets("Captain America")
movie_tweets=cache_top_tweets("Finding Dory")
tweets_tuple= (movie_tweets)
movie_instance_list = get_omdb_data("Captain America")
movie_instance_list=get_omdb_data("Logan")
movie_instance_list=get_omdb_data("Finding Dory")
movie_tuple= (movie_instance_list)

""


######################################################### Loading data into SQL Database ################################
#load the twitter database and then continue to load the movie database as well:


conn = sqlite3.connect('final_project.db')
cur = conn.cursor()
#CREATE TABLE Movies
#Properties: movie_id(primary key), title, director, num_languages, imdb_rating, top_billed_actor
createStatement = 'CREATE TABLE IF NOT EXISTS Movies '
createStatement += '(movie_id TEXT PRIMARY KEY, '
createStatement += 'title TEXT, '
createStatement += 'director INTEGER, '
createStatement += 'num_languages INTEGER, '
createStatement += 'imdb_rating REAL, '
createStatement += 'top_billed_actor TEXT)'
createStatement += 'num_languages INTEGER,'
createStatement += 'imdb_rating REAL, '
createStatement += 'top_billed_actor TEXT)'

conn.commit()
#### Create Tweets Tables
createStatement = 'CREATE TABLE IF NOT EXISTS Tweets '
createStatement += '(text TEXT, '
createStatement += 'tweet_id TEXT PRIMARY KEY, '
createStatement += 'user_id TEXT, '
createStatement += 'movie_id INTEGER, '
createStatement += 'num_favorites INTEGER, '
createStatement += 'num_retweets INTEGER, '
createStatement += 'FOREIGN KEY (user_id) REFERENCES Users(user_id), '
createStatement += 'FOREIGN KEY (movie_id) REFERENCES Movies(movie_id))'
cur.execute(createStatement)
conn.commit()




############### Manipulation ########################
characters_list = [] # all of the characters 

for description in movie_instance_list:
    characters = re.findall(r"[a-zA-Z0-9]", description) #using regX to search for the words
    for character in characters:
        characters_list.append(character)
most_common_char = collections.Counter(characters_list).most_common(1)[0] #using Counter in the Collections Library
print(most_common_char)




def character_count(x):
	return (x[0], len(x[1]))

character_count = map(character_count, movie_tweets)



######################### Output to a file ##########################################
outfile = open('206_final_project.txt', 'w')
outfile.write("Ankita Data \n \n \n \n")

outfile.write("The Movies that I got tweet data on are: \n")
outfile.write("Logan, Captain America, Finding Dory")


outfile.write("most_common_char")
outfile.write("Thank you")
outfile.close()

class Tweets_Test(unittest.TestCase):
	def test_tweets_1(self):
		conn = sqlite3.connect('movie_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=5, "Testing there are at least 5records in the Tweets database")
		conn.close()
	def test_tweets_2(self):
		conn = sqlite3.connect('movie_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==5,"Testing that there are 5 columns in the Tweets table")
		conn.close()
	def test_tweets_3(self):
		conn = sqlite3.connect('movie_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT user_id FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1][0])>=2,"Testing that a tweet user_id value fulfills a requirement of being a Twitter user id rather than an integer, etc")
		conn.close()

class MovieTests(unittest.TestCase):
	# def test_movie_init(self):

	def test_movie_(self):
		dictionary_data = {}
		m = Movie(dictionary_data)
		## test type
		self.assertEqual(type(m.movie_title), type("string"))

	def test_movie_methodself(self):
		dictionary_data = {}
		m = Movie(dictionary_data)
		self.assertEqual(type(m.movie_imdb_rating), type(9.2))

	def test_movie_constructor(self):
		dictionary_data = {}
		m = Movie(dictionary_data)
		self.assertEqual(type(m.movie_director), type("string"))



if __name__ == "__main__":
	unittest.main(verbosity=2)








