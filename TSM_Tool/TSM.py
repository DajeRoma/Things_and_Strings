# -*- coding: utf-8 -*-

import csv
import codecs
import sys
import os
import requests
from nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger

import wiki
import util
from EntityCooccurrence import EntityCooccurrence


reload(sys)  
sys.setdefaultencoding('utf8')

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CANDIDATES_LIST_PATH = os.path.join(CURRENT_DIR_PATH, "candidate_locations_list.csv")
WIKI_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "wikipedia")
WIKI_ENTITIES_PATH = os.path.join(CURRENT_DIR_PATH, "wikipedia_entities.csv")
DB_ENTITIES_PATH = os.path.join(CURRENT_DIR_PATH, "dbpedia_entities.csv")


class TSM:
	def __init__(self, place_name, sentence):
		self.sentence = sentence
		self.ambiguous_place_name = place_name.lower()
		self.candidate_locations = []
		self.candidate_locations_db = []
		self.candidate_locations_wiki = []
		self.candidate_locations_long = []
		self.candidate_locations_lat = []

		self.new_ambiguous_name = False
		self.all_ambiguous_names_list = set()
		self.all_candidates = {}
		self.load_existing_list()
		self.get_candidate_locations()
		self.load_wiki_content()
		self.write_to_candidate_location_list()

		self.all_candidate_locations_wiki_entities = {}
		self.all_candidate_locations_db_entities = {}





	def call_entity_cooccurrence(self):
		ec = EntityCooccurrence()
		for ambi_name in self.all_candidates:
			ec.ambi_name_to_candidates[ambi_name.lower()] = \
				[item.lower() for item in self.all_candidates[ambi_name].keys()]
		ec.load_wiki_entities(WIKI_ENTITIES_PATH)
		ec.load_dbpedia_entities(DB_ENTITIES_PATH)
		if self.new_ambiguous_name is True:
			self._add_entities_for_ec(self)

	def _add_entities_for_ec(self):
		pass





	def write_to_candidate_location_list(self):		
		if self.new_ambiguous_name is False:
			return
		list_of_lists = []
		for i in xrange(len(self.candidate_locations)):
			temp_list = []
			temp_list.append(self.candidate_locations[i])
			temp_list.append(self.ambiguous_place_name.title())
			temp_list.append(self.candidate_locations_wiki[i])
			temp_list.append(self.candidate_locations_db[i])
			temp_list.append(self.candidate_locations_lat[i])
			temp_list.append(self.candidate_locations_long[i])
			list_of_lists.append(temp_list)
		with open(CANDIDATES_LIST_PATH, 'a') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for listEntry in list_of_lists:
				spamwriter.writerow(listEntry)
		print "Candidate location list updated"
		


	def load_existing_list(self):
		table = util.read_listOfList_from_CSV(CANDIDATES_LIST_PATH)
		for row in table:
			ambi_name = row[1].lower()
			if ambi_name not in self.all_ambiguous_names_list:
				self.all_ambiguous_names_list.add(ambi_name)
				self.all_candidates[ambi_name] = {}
			temp_dict = {}
			temp_dict["wiki"] = row[2]
			temp_dict["db"] = row[3]
			temp_dict["long"] = row[4]
			temp_dict["lat"] = row[5]
			self.all_candidates[ambi_name][row[0]] = temp_dict
		print "Existing list loaded"


	def load_wiki_content(self):
		if self.new_ambiguous_name is False \
			or os.path.isdir(os.path.join(WIKI_DIR_PATH, self.ambiguous_place_name)):
			print "Wikipedia texts have been downloaded..."
			return
		else:
			print "!!!!"
			os.makedirs(os.path.join(WIKI_DIR_PATH, self.ambiguous_place_name))
			print "Downloading Wikipedia text..."
			wiki.write_cities_wikis_to_disk(self.candidate_locations, 
									[self.ambiguous_place_name] * len(self.candidate_locations),
									parent_dir=WIKI_DIR_PATH)
			print "Wikipedia texts have been downloaded..."


	# [u'Washington, Arkansas', u'Washington, Connecticut', ...]
	def get_candidate_locations(self):
		if self.ambiguous_place_name in self.all_ambiguous_names_list:
			self.new_ambiguous_name = False
			self.candidate_locations = self.all_candidates[self.ambiguous_place_name].keys()
			for loc in self.candidate_locations:
				self.candidate_locations_wiki.append(self.all_candidates[self.ambiguous_place_name][loc]["wiki"])				
				self.candidate_locations_db.append(self.all_candidates[self.ambiguous_place_name][loc]["db"])
				self.candidate_locations_long.append(self.all_candidates[self.ambiguous_place_name][loc]["long"])
				self.candidate_locations_lat.append(self.all_candidates[self.ambiguous_place_name][loc]["lat"])
			print "Candidate locations loaded"
			return
		self.new_ambiguous_name = True
		locations_db = []
		locations_wiki = []
		locations = []

		query = """select distinct ?a, ?b, ?c where {
				?a rdfs:label ?c.
				?b foaf:primaryTopic ?a.
				?a rdf:type ?e.
				?a geo:geometry ?d.
				filter (STRSTARTS(LCASE(STR(?c)), \"""" + self.ambiguous_place_name + """,\") || LCASE(STR(?c)) = \"""" + self.ambiguous_place_name + """\").
				filter(?e IN (dbo:Town, dbo:City, dbo:Settlement))}
				LIMIT 30
		"""
		parameters = {'query': query, 'format': 'json'}
		sparqlRequest = requests.get('http://dbpedia.org/sparql', params = parameters)
		# print sparqlRequest.json()
		results = sparqlRequest.json()["results"]["bindings"]
		# print results
		# in case "redirected"
		for result in results:
			if result['a']['value'] in locations_db:
				continue
			locations_db.append(result['a']['value'])
			locations_wiki.append(result['b']['value'])
			locations.append(result['c']['value'])
		self.candidate_locations = locations
		self.candidate_locations_db = locations_db
		self.candidate_locations_wiki = locations_wiki
		# print self.candidate_locations
		self.get_candidate_locations_coor()
		print "Candidate locations loaded"
		return


	def get_candidate_locations_coor(self):
		if self.ambiguous_place_name in self.all_ambiguous_names_list:
			return
		new_candidate_locations = []
		new_candidate_locations_db = []
		new_candidate_locations_wiki = []
		for i in xrange(len(self.candidate_locations_db)):
			candidate_db = self.candidate_locations_db[i]
			prefix = "PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>"
			query = prefix + """SELECT (str(?geom) AS ?g) (strlen(?g) AS ?len) 
								WHERE {<""" + candidate_db + """> geo:geometry ?geom} 
								ORDER BY DESC(?len)"""
			parameters = {'query': query, 'format': 'json'}
			sparqlRequest = requests.get('http://dbpedia.org/sparql', params = parameters)
			# print sparqlRequest.json()
			results = sparqlRequest.json()["results"]["bindings"]
			if len(results) == 0:
				print candidate_locations[i], "has no coordinates"
				return
			point_coor = results[0]['g']['value'][6:-1].split(' ')
			lat, lng = point_coor[1], point_coor[0]
			self.candidate_locations_long.append(lng)
			self.candidate_locations_lat.append(lat)
			new_candidate_locations.append(self.candidate_locations[i])
			new_candidate_locations_db.append(self.candidate_locations_db[i])
			new_candidate_locations_wiki.append(self.candidate_locations_wiki[i])
		self.candidate_locations = new_candidate_locations
		self.candidate_locations_db = new_candidate_locations_db
		self.candidate_locations_wiki = new_candidate_locations_wiki
		return


	# Returns:
	# annotated_word_list => [(u'Washington', u'LOCATION'), (u',', 'O'), (u'D.C.', u'LOCATION'), (u', formally the', 'O'), (u'District of Columbia', u'LOCATION'), (u'and commonly referred to as ``', 'O'), (u'Washington', u'LOCATION'), (u"'' , `` the District '' , or simply `` D.C. '' , is the capital of the", 'O'), (u'United States', u'LOCATION'), (u'.', 'O')]
	# word_list => [u'Washington', u',', u'D.C.', u', formally the', u'District of Columbia', u'and commonly referred to as ``', u'Washington', u"'' , `` the District '' , or simply `` D.C. '' , is the capital of the", u'United States', u'.']
	# locations_indices => [0, 2, 4, 6, 8]
	@staticmethod
	def named_emtity_recognition(sentence):
		if not sentence:
			return [], [], []
		classifier = os.path.join(CURRENT_DIR_PATH, "english.all.3class.distsim.crf.ser.gz")
		jar = os.path.join(CURRENT_DIR_PATH, "stanford-ner.jar")
		tagger = StanfordNERTagger(classifier, jar)		 
		sentence = word_tokenize(sentence)
		tags = tagger.tag(sentence)
		# print tags
		annotated_word_list = []
		last_word = ""
		last_tag = ""
		for i in xrange(len(tags)):
			word = tags[i][0]			
			tag = tags[i][1] if tags[i][1] == "LOCATION" else "O"
			if i == 0:
				last_word = word
				last_tag = tag
			else:
				if tag == last_tag:
					last_word += " " + word
				else:
					annotated_word_list.append((last_word.strip(), last_tag))
					last_word = word
				last_tag = tag
		if len(tags) > 0 and last_word != "":
			annotated_word_list.append((last_word.strip(), last_tag))

		word_list = []
		locations_indices = []
		for i in xrange(len(annotated_word_list)):
			word_list.append(annotated_word_list[i][0])
			if annotated_word_list[i][1] == "LOCATION":
				locations_indices.append(i)
		return annotated_word_list, word_list, locations_indices




	






if __name__ == "__main__":
	# short_text = """Washington, D.C., formally the District of Columbia and commonly referred to as "Washington", "the District", or simply "D.C.", is the capital of the United States."""
	# print TSM.named_emtity_recognition(short_text)


	tsm = TSM("washington")
	# tsm.get_candidate_locations()
	# tsm.load_wiki_content()
	# tsm.get_candidate_locations()