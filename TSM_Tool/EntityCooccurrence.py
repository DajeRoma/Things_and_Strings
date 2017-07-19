# -*- coding: utf-8 -*-

import csv
from bs4 import BeautifulSoup
from bs4 import element
import urllib2
import contextlib
import os
import re
import sys
import requests
from nltk.tokenize import word_tokenize
from math import log


reload(sys)  
sys.setdefaultencoding('utf8')

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CANDIDATES_LIST_CSV_FILE_PATH = os.path.join(
									os.path.dirname(CURRENT_DIR_PATH), 
									"training_data",
									"wiki_most_common_us_place_name_double_cleaned.csv")

class EntityCooccurrence:
	def __init__(self):
		self.model = None
		self.ambi_name_to_candidates = {}
		self.candidate_wiki_url = {}
		self.candidate_wiki_entities = {}
		self.candidate_db_entities = {}
		self.load_candidate_list()


	def load_candidate_list(self, candidateFilePath=CANDIDATES_LIST_CSV_FILE_PATH):
		with open(candidateFilePath, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in spamreader:
				candidate = row[0].lower()
				ambi_name = row[1].lower()
				wiki = row[2]
				if ambi_name in self.ambi_name_to_candidates:
					self.ambi_name_to_candidates[ambi_name].append(candidate)
				else:
					self.ambi_name_to_candidates[ambi_name] = [candidate]
				self.candidate_wiki_url[candidate] = wiki


	def load_wiki_entities(self, wiki_file_path):
		with open(wiki_file_path, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in spamreader:
				self.candidate_wiki_entities[row[0].lower()] = set(lower_list_string(row[1:]))


	def load_dbpedia_entities(self, db_file_path):
		with open(db_file_path, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in spamreader:
				self.candidate_db_entities[row[0].lower()] = set(lower_list_string(row[1:]))


	def apply_model(self, testing_sent, ambi_name):
		if not self.ambi_name_to_candidates:
			print "[error] have to load candidate list first"
			return
		if not self.candidate_wiki_entities:
			print "[error] have to load wikipedia entities"
			return
		if not self.candidate_db_entities:
			print "[error] have to load dbpedia entities"
			return
		candidate_places = self.ambi_name_to_candidates[ambi_name]
		if ambi_name in testing_sent:
			testing_sent = testing_sent.replace(ambi_name, "")
		candidates_wiki_entities = {}
		candidates_db_entities = {}
		testing_words = word_tokenize(testing_sent.lower())
		for candidate_place in candidate_places:
			candidates_wiki_entities[candidate_place] = {}
			candidates_db_entities[candidate_place] = {}
		for word in testing_words:	
			for candidate_place in candidate_places:
				# print self.candidate_wiki_entities[candidate_place]
				if word in self.candidate_wiki_entities[candidate_place]:
					candidates_wiki_entities[candidate_place][word] = 1
				if word in self.candidate_db_entities[candidate_place]:
					candidates_db_entities[candidate_place][word] = 1
		# print candidates_wiki_entities
		candidates_tf = self.get_tf(candidates_wiki_entities, candidates_db_entities)
		# print candidates_tf
		entities_idf = self.get_idf(candidates_wiki_entities, candidates_db_entities)
		# print entities_idf
		candidates_tfiidf = self.get_tf_idf_helper(candidates_tf, entities_idf)
		return candidates_tfiidf

	
	"""
		Get the Term Frequency for each candidate place's every entity
	"""
	@staticmethod
	def get_tf(candidates_wiki_entities, candidates_db_entities):
		candidates_tf = {}
		for candidate in candidates_wiki_entities:
			candidates_tf[candidate] = {}
			for entity in candidates_wiki_entities[candidate]:
				candidates_tf[candidate][entity] = 1
			for entity in candidates_db_entities[candidate]:
				if entity in candidates_tf[candidate]:
					candidates_tf[candidate][entity] = 2
				else:
					candidates_tf[candidate][entity] = 1
		return candidates_tf


	"""
		Get the Inverse Document Frequency for every entity
	"""
	@staticmethod
	def get_idf(candidates_wiki_entities, candidates_db_entities):
		entities_count = {}
		for candidate in candidates_wiki_entities:
			for entity in candidates_wiki_entities[candidate]:
				if entity in entities_count:
					entities_count[entity] += 1
				else:
					entities_count[entity] = 1
			for entity in candidates_db_entities[candidate]:
				if entity in entities_count:
					entities_count[entity] += 1
				else:
					entities_count[entity] = 1
		the_E = len(candidates_wiki_entities.keys())
		entities_idf = {}
		for entity in entities_count:
			entities_idf[entity] = 1 + log((the_E + 1) / entities_count[entity])
		return entities_idf


	"""
		Get the Entity Co-occurrence Model's final score (TF-IDF) 
		  for each candidate place
	"""
	@staticmethod
	def get_tf_idf_helper(candidates_tf, entities_idf):
		candidate_scores = {}
		for candidate in candidates_tf:
			temp_score = 0
			for entity in candidates_tf[candidate]:
				temp_score = 1.0 * candidates_tf[candidate][entity] * entities_idf[entity]
			candidate_scores[candidate] = temp_score
		return candidate_scores
		


def lower_list_string(listOfString):
	list_to_return = []
	for string in listOfString:
		list_to_return.append(string.lower())
	return list_to_return


"""
	Given an url of a candidate place's wikipedia page, find all entities
"""
def get_wiki_entities_from_url(url):
	entityList = []
	uniqueEntity = []
	# read links (close after done with the link)
	with contextlib.closing(urllib2.urlopen(url)) as webPage:
		webPageHTML = webPage.read()
		# use bs library to process the page
		soup = BeautifulSoup(webPageHTML, "lxml")
		# find all p tags (paragraphs) since entities will only show up in paragraphs
		pList = soup.find_all("p")
		for paragraph in pList:
			# each paragraph contains string, and other tags (these are the children of the p)
			for child in paragraph.children:
				# if the child is a Tag (not a string)
				if isinstance(child, element.Tag):
					# if the Tag has a link (<a>) and "wiki" is in the link (which means this is a wiki page)
					if "href" in child.attrs and "title" in child.attrs and (child["href"]).startswith("/wiki"):
						if child["href"] in uniqueEntity:
							continue
						uniqueEntity.append(child["href"])
						# print child["href"]
						# print child["title"]
						# store multiple forms of the same entity
						tempString = ""
						# the title attr of the link is one form
						tempString = tempString + child["title"]
						# the text of the link could be another form
						if child["title"] is not None and child.string is not None:
							if child.string.lower() != child["title"].lower():
								# use ";" as delimiter
								tempString = tempString + ";" + child.string
						# check possible redirect links (forms)
						checkRedirURL = "https://en.wikipedia.org" + child["href"]
						with contextlib.closing(urllib2.urlopen(checkRedirURL)) as webPageRe:
							webPageReHTML = webPageRe.read()
							soupRe = BeautifulSoup(webPageReHTML, "lxml")
							# redirects are in the div tag
							divList = soupRe.find_all("div")
							for div in divList:
								# redirects/redirect
								if "role" in div.attrs and div["role"] == "note" and ("redirects here" in str(div) or "redirect here" in str(div)):
									# print checkRedirURL
									for item in div.children:
										# check if it's a string
										if isinstance(item, element.NavigableString):
											# e.g. "SoCal" and "Socal" redirect here. extract everything that is double quoted
											if "redirect here" in item or "redirects here" in item:
												tempList = re.findall(r'"([^"]*)"', item)
												tempString = tempString + ";" + ";".join(tempList)
									# print tempString
						if ";" in tempString:
							for item in tempString.split(";"):
								# print item.strip()
								entityList.append(item.strip().lower())
						else:
							# print tempString.strip()
							entityList.append(tempString.strip().lower())
	# print len(entityList)
	# print len(uniqueEntity)
	listToReturn = []
	for entity in uniqueEntity:
		listToReturn.append(entity[6:].replace('_', ' '))
	return listToReturn


"""
	Given an url of a candidate place's DBpedia page, find all entities
"""
def get_db_entities_from_url(url):
	entities = set()
	# url = "http://en.wikipedia.org/wiki/Washington,_D.C."
	if "https" in url:
		url = url.replace("https", "http")
	query = """select *
				{
				  {
					select ?a ?b ?c
					where {
						   <""" + url + """> foaf:primaryTopic ?a.
						   ?a ?b ?c.
						   FILTER(STRSTARTS(STR(?b), "http://dbpedia.org/ontology/") || STRSTARTS(STR(?b), "http://dbpedia.org/property/")).
						   FILTER(!isLiteral(?c)).
					}
				  }
				  union
				  {
					select ?c ?b ?a
					where {
						   <""" + url + """> foaf:primaryTopic ?a.
						   ?c ?b ?a.
						   FILTER(STRSTARTS(STR(?b), "http://dbpedia.org/ontology/") || STRSTARTS(STR(?b), "http://dbpedia.org/property/")).
						   FILTER(!isLiteral(?c)).
					}
				  }
				}
	"""
	parameters = {'query': query, 'format': 'json'}
	sparqlRequest = requests.get('http://dbpedia.org/sparql', params = parameters)
	# print sparqlRequest.json()
	results = sparqlRequest.json()["results"]["bindings"]
	# in case "redirected"
	if len(results) == 1 and results[0]['b']['value'] == "http://dbpedia.org/ontology/wikiPageRedirects":
		redirct_url = results[0]['c']['value']
		redirct_url = redirct_url.replace("http://dbpedia.org/resource/", "http://en.wikipedia.org/wiki/")
		return get_db_entities_from_url(redirct_url)
	for result in results:
		obj = result['c']['value']
		if "http://dbpedia.org/resource/" in obj:
			entity = obj[len("http://dbpedia.org/resource/"):]
			entity = entity.replace('_', " ")
			if '(' in entity:
				entity = entity[:entity.find('(')]
			entity = entity.strip()
			entities.add(entity)
			# print entity
	return list(entities)


def write_entities_to_csv(places, entities, csvFilePath):
	print len(places), len(entities)
	assert len(places) == len(entities), "length of places and entities should be matching"
	with open(csvFilePath, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in xrange(len(places)):
			spamwriter.writerow([places[i]] + entities[i])
	return


def do_batch_wiki():
	ec = EntityCooccurrence()
	place_list = []
	wiki_entities = []
	counter = 0
	for candidate in ec.candidate_wiki_url:
		counter += 1
		print counter,		
		place_list.append(candidate)
		wiki_entity = get_wiki_entities_from_url(ec.candidate_wiki_url[candidate])
		wiki_entities.append(wiki_entity)
		print candidate
	output_file_path = os.path.join(CURRENT_DIR_PATH, "wikipedia_entities.csv")
	write_entities_to_csv(place_list, wiki_entities, output_file_path)


def do_batch_db():
	ec = EntityCooccurrence()
	place_list = []
	db_entities = []
	counter = 0
	for candidate in ec.candidate_wiki_url:
		counter += 1
		print counter,		
		place_list.append(candidate)
		db_entity = get_db_entities_from_url(ec.candidate_wiki_url[candidate])
		db_entities.append(db_entity)
		print candidate
	output_file_path = os.path.join(CURRENT_DIR_PATH, "dbpedia_entities.csv")
	write_entities_to_csv(place_list, db_entities, output_file_path)








if __name__ == "__main__":
	# print get_wiki_entities_from_url("https://en.wikipedia.org/wiki/Washington,_District_of_Columbia")

	# print get_db_entities_from_url("https://en.wikipedia.org/wiki/Washington,_District_of_Columbia")

	# do_batch_wiki()
	# do_batch_db()


	ec = EntityCooccurrence()
	ec.load_wiki_entities(os.path.join(CURRENT_DIR_PATH, "wikipedia_entities.csv"))
	ec.load_dbpedia_entities(os.path.join(CURRENT_DIR_PATH, "dbpedia_entities.csv"))
	testing_sent = "colony the town of washington assessor is responsible for appraising real estate and assessing a property tax on properties located in town of washington, ."
	ambi_name = "washington"
	ec.apply_model(testing_sent, ambi_name)
