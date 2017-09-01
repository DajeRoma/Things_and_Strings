#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import csv
import os
import re
import sys
import time
import util

from bs4 import BeautifulSoup
import nltk.data
import urllib2
import wikipedia


reload(sys)  
sys.setdefaultencoding('utf8')

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
WIKIPEDIA_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "wikipedia")


URL_MOST_COMMON_US_PLACE_NAME = "https://en.wikipedia.org/wiki/List_of_the_most_common_U.S._place_names"
# MOST_COMMON_PLACE_NAME_CSV_FILE = os.path.join(CURRENT_DIR_PATH, "wiki_most_common_us_place_name_cleaned.csv")
MOST_COMMON_PLACE_NAME_CSV_FILE = os.path.join(CURRENT_DIR_PATH, "wiki_most_common_us_place_name_double_cleaned.csv")


def grab_wiki_most_common_us_place_name(url=URL_MOST_COMMON_US_PLACE_NAME):
	webPageHTML = urllib2.urlopen(url).read()
	soup = BeautifulSoup(webPageHTML, "html.parser")
	tables = soup.find_all("table", attrs={"class": "wikitable"})
	assert len(tables)==32  # should be 32
	tableContent = []
	for table in tables:
		trs = table.find_all("tr")
		for row in trs[1:]:
			tds = row.find_all("td")
			assert len(tds)==2
			if "/wiki/" in tds[0].find("a")["href"]:
				record = [tds[0].get_text(), "https://en.wikipedia.org"+tds[0].find("a")["href"], tds[1].get_text()]
				# record = [td.get_text() for td in row.find_all("td")]
				tableContent.append(record)
	# for i in tableContent:
	# 	print i
	return tableContent


"""
	Return two lists:
	  1. Most common US place names in ambiguous form (with duplicates), e.g., Washington; Springfield
	  2. Most common US place names in disambiguous form, e.g., Washington, Geogia; Oakland, California
"""
def get_most_common_us_place_names_lists(commonPlaceNamesCSVFile=MOST_COMMON_PLACE_NAME_CSV_FILE):
	placeNamesAmbiguous = []
	placeNamesDisambiguous = []
	listOfList = util.read_listOfList_from_CSV(commonPlaceNamesCSVFile)
	assert len(listOfList)>0
	assert len(listOfList[0])==2
	for theList in listOfList:
		placeNamesAmbiguous.append(theList[1])
		placeNamesDisambiguous.append(theList[0])
	return placeNamesAmbiguous, placeNamesDisambiguous


"""
	Feed place names to Wikipedia API to see if have validate names
"""
def validate_place_names_with_wiki(placeNameList):
	counter = 1
	for placeName in placeNameList:
		print counter,
		counter+=1
		if not wiki.get_wiki_content(placeName):
			print placeName


"""
	Create folders on the disk for each city in the cities
"""
def create_dir_for_cities(cities, parent_dir=WIKIPEDIA_DIR_PATH):
	for city_name in cities:
		if not os.path.exists(os.path.join(parent_dir, city_name)):
			os.makedirs(os.path.join(parent_dir, city_name))


"""
	Write wikipedia content to the disk
	  dirctory: {parent_dir}/{ambi_city_name}/....txt
"""
def write_cities_wikis_to_disk(cities, 
								ambi_cities,
								parent_dir=WIKIPEDIA_DIR_PATH):
	print cities
	print ambi_cities
	assert len(cities)==len(ambi_cities)
	for i in xrange(len(cities)):
		print cities[i]
		cleaned_wiki_sents = wiki.clean_wiki_content(
								wiki.get_wiki_content(cities[i]))
		util.write_listOfStrings_to_txt(
						cleaned_wiki_sents, 
						os.path.join(parent_dir,
									ambi_cities[i],
									cities[i].replace(" ", "_")+".txt"))


"""
	Read text from a file and return with a string
"""
def read_from_txt_to_str(txt_file_path):
	with codecs.open(txt_file_path, 'rb', encoding='utf8') as outfile:
		line_list = outfile.readlines()
	line_list = [line.strip() for line in line_list]
	# print len(line_list)
	return "\n".join(line_list).strip()


def read_listOfList_from_CSV(csv_file_path):
		listOfList = []
		with open(csv_file_path, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in spamreader:
				listOfList.append(row)
		return listOfList





class wiki:
	def __init__(self):
		# ["Washington", "Springfield", ...]
		self.ambi_place_names_list = self._get_ambiguous_place_name_list()
		# ["Washington, Georgia": "Washington", "Washington, Akansas": "Washington", ...]
		self.place_name_dictionary = self._get_place_place_name_map()



	def _get_ambiguous_place_name_list(self, wikiFolderPath=WIKIPEDIA_DIR_PATH):
		return os.listdir(wikiFolderPath)


	def _get_place_place_name_map(self, wikiFolderPath=WIKIPEDIA_DIR_PATH):
		place_map_to_ambi_place_name = {}
		for folder in os.listdir(wikiFolderPath):
			for wiki_file in os.listdir(os.path.join(wikiFolderPath, folder)):
				place = wiki_file[:wiki_file.index(".txt")].replace('_', ' ')
				place_map_to_ambi_place_name[place] = folder
		return place_map_to_ambi_place_name


	def get_all_ambi_places(self):
		return self.ambi_place_names_list


	def get_candidate_places(self, place_name, filter_option=True):
		if place_name not in self.ambi_place_names_list:
			print "[Warning] this place name \"" + place_name + "is not found"
			return []
		candidate_places = []
		filter_list = self.get_filter_list()
		for key in self.place_name_dictionary:
			if filter_option == True and key not in filter_list:
				continue
			if self.place_name_dictionary[key] == place_name:
				candidate_places.append(key)
		return candidate_places


	def get_candidate_places_file_path(self, place_name, filter_option=True):
		if place_name not in self.ambi_place_names_list:
			print "[Warning] this place name \"" + place_name + "is not found"
			return []
		candidate_places_files_path = []
		filter_list = self.get_filter_list()
		for key in self.place_name_dictionary:
			if filter_option == True and key not in filter_list:
				continue
			if self.place_name_dictionary[key] == place_name:
				temp_file_path = os.path.join(WIKIPEDIA_DIR_PATH, place_name, str(key.replace(' ', '_')) + ".txt")
				if self.validate_file_path(temp_file_path):
					candidate_places_files_path.append(temp_file_path)
				else:
					print "[Warning] The file path is invalid. ", temp_file_path
		return candidate_places_files_path





	"""
		Read the wiki_most_common_us_place_name_(double)_cleaned.csv_file_path
			and get our vocabulary of candiate place names
	"""
	@staticmethod
	def get_filter_list(wiki_place_file=MOST_COMMON_PLACE_NAME_CSV_FILE):
		city_placeName = read_listOfList_from_CSV(wiki_place_file)
		filter_list = []
		for item in city_placeName:
			filter_list.append(item[0])
		return filter_list


	@staticmethod
	def read_wiki_content_as_str(filePath):
		return read_from_txt_to_str(filePath)


	@staticmethod
	def validate_file_path(file_Path):
		return os.path.exists(file_Path)


	"""
	Search by a keyword; return by a list of wiki entities
	  sample: [u'Washington', u'Washington (state)', u'Denzel Washington', u'Washington Monument', u'George Washington', u'The Washington Post', u'University of Washington', u'Washington Nationals', u'Washington, Pennsylvania', u'List of Governors of Washington']
	"""
	@staticmethod
	def search(keyword):
		return wikipedia.search(keyword)


	"""
	Given a keyword, if it has a disambiguation page, return a list of entities
	  otherwise, return the page of the entity of the keyword
	"""
	@staticmethod
	def get_disambiguation_list(keyword):
		try:
			wikipage = wikipedia.page(keyword)
			print "No disambiguation"
			return wikipage
		except Exception as e:
			exceptInfo = str(e)
			# print exceptInfo
			entityList = exceptInfo.split('\n')
			return entityList[1:-2]


	@staticmethod
	def get_wiki_content(entity):
		try:
			return wikipedia.page(entity).content.encode('utf-8')
		except Exception as e:
			time.sleep(5)
			try:
				return wikipedia.page(entity).content.encode('utf-8')
			except Exception as e1:
				print '"'+entity+'" is ambiguous'
				print str(e1)
				return ""


	"""
		Clean the text
		  return a list of sentences
	"""
	@staticmethod
	def clean_wiki_content(wikiContent):
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		sents = sent_detector.tokenize(wikiContent.strip())
		newSents = []
		for sent in sents:
			# todo
			# should revise
			sent = re.sub('^={2}[\sA-Za-z]+={2}', '', sent)
			sent = re.sub('=={1,4}', '', sent)
			sentList = sent.split('\n')
			for sentEntry in sentList:
				sentEntry = sentEntry.strip()
				if len(sentEntry)>0:
					newSents.append(sentEntry)
		# print len(sents), len(newSents)
		# counter = 1
		# for sent in newSents:
		# 	print counter, sent
		# 	counter +=1
		return newSents



if __name__ == '__main__':
	# print wiki.search("Lexington, North Carolina")
	# for entry in wiki.get_disambiguation_list("washington"):
	# 	wiki.get_wiki_content(entry)
	# cleaned_wiki_sents = wiki.clean_wiki_content(
	# 			wiki.get_wiki_content("Washington, District of Columbia"))
	# print wiki.get_wiki_content("Milford, Connecticut")
	# print wiki.get_wiki_content("Washington, District of Columbia")


	# placeNameList = grab_wiki_most_common_us_place_name()
	# util.write_listOfList_to_CSV(placeNameList, os.path.join(CURRENT_DIR_PATH, "wiki_most_common_us_place_name.csv"))

	# ambiguousPlaceName, disambiguousPlaceName = get_most_common_us_place_names_lists()
	# validate_place_names_with_wiki(disambiguousPlaceName)

	# create_dir_for_cities(ambiguousPlaceName)

	# write_cities_wikis_to_disk(disambiguousPlaceName, ambiguousPlaceName)


	# print re.sub('^={2}[\sA-Za-z]+={2}', '', "== Notes ==    ")

	# wk = wiki()
	# all_ambi_places = wk.get_all_ambi_places()
	# for place in wk.get_all_ambi_places():
	# 	wk.get_candidate_places_file_path(place)

	wiki.read_wiki_content_as_str("/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/wikipedia/Washington/Washington,_District_of_Columbia.txt")
