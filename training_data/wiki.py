import util

import wikipedia
from bs4 import BeautifulSoup
import urllib2
import os
import time
import nltk.data
import re


current_dir_path = os.path.dirname(os.path.realpath(__file__))
wikipedia_dir_path = os.path.join(current_dir_path, "wikipedia")


URL_MOST_COMMON_US_PLACE_NAME = "https://en.wikipedia.org/wiki/List_of_the_most_common_U.S._place_names"
MOST_COMMON_PLACE_NAME_CSV_FILE = os.path.join(current_dir_path, "wiki_most_common_us_place_name_cleaned1.csv")



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
def create_dir_for_cities(cities, parent_dir=wikipedia_dir_path):
	for city_name in cities:
		if not os.path.exists(os.path.join(parent_dir, city_name)):
			os.makedirs(os.path.join(parent_dir, city_name))


"""
	Write wikipedia content to the disk
	  dirctory: {parent_dir}/{ambi_city_name}/....txt
"""
def write_cities_wikis_to_disk(cities, 
								ambi_cities,
								parent_dir=wikipedia_dir_path):
	assert len(cities)==len(ambi_cities)
	for i in xrange(565, len(cities)):
		print cities[i]
		cleaned_wiki_sents = wiki.clean_wiki_content(
								wiki.get_wiki_content(cities[i]))
		util.write_listOfStrings_to_txt(
						cleaned_wiki_sents, 
						os.path.join(parent_dir,
									ambi_cities[i],
									cities[i].replace(" ", "_")+".txt"))




class wiki:
	def __init__(self):
		pass


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
				return None


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
	# util.write_listOfList_to_CSV(placeNameList, os.path.join(current_dir_path, "wiki_most_common_us_place_name.csv"))

	ambiguousPlaceName, disambiguousPlaceName = get_most_common_us_place_names_lists()
	# validate_place_names_with_wiki(disambiguousPlaceName)

	# create_dir_for_cities(ambiguousPlaceName)

	write_cities_wikis_to_disk(disambiguousPlaceName, ambiguousPlaceName)


	# print re.sub('^={2}[\sA-Za-z]+={2}', '', "== Notes ==    ")