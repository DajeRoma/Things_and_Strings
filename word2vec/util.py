# -*- coding: utf-8 -*-

import csv
import codecs
import sys
import nltk.data
from nltk.tokenize import WordPunctTokenizer, word_tokenize


reload(sys)  
sys.setdefaultencoding('utf8')


def write_listOfList_to_CSV(listOfList, csv_file_path):
	with open(csv_file_path, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for listEntry in listOfList:
			spamwriter.writerow(listEntry)


def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList


def write_listOfStrings_to_txt(listOfStrings, txt_file_path):
	with codecs.open(txt_file_path, 'w', encoding='utf8') as outfile:
		for string in listOfStrings:
			string = string.decode('utf-8', errors='replace').encode('utf-8')
			outfile.write(string + '\n')


"""
	Given a string, tokenize the string into a list of sentences
		Punkt Sentence Tokenizer
"""
def tokenize_to_sents(text):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sents = [sent.strip() for sent in sent_detector.tokenize(text.strip())]
	return sents


"""
	Given a string, tokenize the string (a sentence) into a list of words
		Punkt Word Tokenizer
"""
def tokenize_sent_to_words(sent):
	return word_tokenize(sent)


"""
	Given a string, tokenize the string (one or multiple sentences) into 
	  a list of sentences first and then to words
		Punkt Sentence Tokenizer + Punkt Word Tokenizer
"""
def tokenized_to_words(text):
	words = []
	for sent in tokenize_to_sents(text):
		words.extend(tokenize_sent_to_words(sent))
	return words



if __name__ == "__main__":
	sent1 = """Washington, D.C., formally the District of Columbia and commonly referred to as "Washington", "the District", or simply "D.C.", is the capital of the United States.
		The signing of the Residence Act on July 16, 1790, approved the creation of a capital district located along the Potomac River on the country's East Coast.
		The U.S. Constitution provided for a federal district under the exclusive jurisdiction of the Congress and the District is therefore not a part of any state.
		The states of Maryland and Virginia each donated land to form the federal district, which included the pre-existing settlements of Georgetown and Alexandria.
		Named in honor of President George Washington, the City of Washington was founded in 1791 to serve as the new national capital.
		In 1846, Congress returned the land originally ceded by Virginia; in 1871, it created a single municipal government for the remaining portion of the District.
		Washington had an estimated population of 681,170 as of July 2016.
		Commuters from the surrounding Maryland and Virginia suburbs raise the city's population to more than one million during the workweek.
		The Washington metropolitan area, of which the District is a part, has a population of over 6 million, the sixth-largest metropolitan statistical area in the country.
		The centers of all three branches of the federal government of the United States are in the District, including the Congress, President, and Supreme Court.
		Washington is home to many national monuments and museums, which are primarily situated on or around the National Mall.
		The city hosts 176 foreign embassies as well as the headquarters of many international organizations, trade unions, non-profit organizations, lobbying groups, and professional associations.
		A locally elected mayor and a 13‑member council have governed the District since 1973.
		However, the Congress maintains supreme authority over the city and may overturn local laws.
		D.C. residents elect a non-voting, at-large congressional delegate to the House of Representatives, but the District has no representation in the Senate.
		The District receives three electoral votes in presidential elections as permitted by the Twenty-third Amendment to the United States Constitution, ratified in 1961.
		Various tribes of the Algonquian-speaking Piscataway people (also known as the Conoy) inhabited the lands around the Potomac River when Europeans first visited the area in the early 17th century.
		One group known as the Nacotchtank (also called the Nacostines by Catholic missionaries) maintained settlements around the Anacostia River within the present-day District of Columbia.
		Conflicts with European colonists and neighboring tribes forced the relocation of the Piscataway people, some of whom established a new settlement in 1699 near Point of Rocks, Maryland.
	"""
	# for sent in tokenize_sent(sent1):
	# 	print sent
	# for word in tokenize_sent_to_words(sent1):
	# 	print word
	for word in tokenized_to_words(sent1):
		print word