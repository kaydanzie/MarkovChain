'''
Authors: Kayla Ziegler, Adrienne Bergh, Andrew Krager
-Reads CSV with song lyrics
-generate_song takes list of songs and size of song to be randomly generated
'''
import csv
import re
import random

def generate_song(songList, songSize):
	allSongs = songList

	#keys = single word
	#values = list of words that follow the key
	frequencies = {}
	ho_frequencies = {}

	for song in allSongs:

		#split by all punctuation except apostrophe
		song = re.findall(r"[\w']+", song)

		#remove unicode characters from list
		bad_chars = re.compile(r"x[a-z|0-9]+")
		song = [bad_chars.sub("", item) for item in song]

		for idx, word in enumerate(song):
			#strictly less than length
			if word in frequencies and (idx+1)<len(song):
				frequencies[word].append(song[idx+1]) #append next word in song
				ho_frequencies[word].append(song[idx+1])
				if (idx+2)<len(song):
					ho_frequencies[word].append(song[idx+2])
			#if not last word but not in frequencies yet
			elif (idx+1)<len(song):
				frequencies[word] = [song[idx+1]]
				ho_frequencies[word] = [song[idx+1]]
				if (idx+2)<len(song):
					ho_frequencies[word].append(song[idx+2])
			#else you're on the last word, don't do anything

	random.seed(2)
	randSongF = []
	randSongH = []
	for i in range(songSize):
		#first word in song is random
		if len(randSongF) == 0:
			#first order
			allWordsF = list(frequencies.keys())
			randSongF.append(allWordsF[random.randint(0,len(allWordsF)-1)])
			#higher order
			allWordsH = list(ho_frequencies.keys())
			randSongH.append(allWordsH[random.randint(0,len(allWordsH)-1)])
		else:
			#first order
			#use prev word to predict next word, pick randomly from frequencies
			prevWordF = randSongF[len(randSongF)-1]
			possibleWordsF = frequencies[prevWordF]
			randSongF.append(possibleWordsF[random.randint(0,len(possibleWordsF)-1)])
			#higher order
			prevWordH = randSongH[len(randSongH)-1]
			possibleWordsH = ho_frequencies[prevWordH]
			randSongH.append(possibleWordsH[random.randint(0,len(possibleWordsH)-1)])

	print("FO MARKOV:")
	print(" ".join(randSongF))

	print("HO MARKOV:")
	print(" ".join(randSongH))

all_songs = []
with open('songlyrics.csv', 'rU') as songsFile:
	songreader = csv.reader(songsFile)
	for row in songreader:
		all_songs.append(str(row))

generate_song(all_songs, 100)
