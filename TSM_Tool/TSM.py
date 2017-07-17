# -*- coding: utf-8 -*-

import csv
import codecs
import sys
import os
import requests
from nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger


reload(sys)  
sys.setdefaultencoding('utf8')

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class TSM:
	def __init__(self, place_name):
		self.ambiguous_place_name = place_name.lower()
		self.candidate_locations = []
		self.candidate_locations_db = []
		self.candidate_locations_wiki = []


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




	# [u'Washington, Arkansas', u'Washington, Connecticut', ...]
	def get_candidate_locations(self):
		locations_db = []
		locations_wiki = []
		locations = []

		query = """select distinct ?a, ?b, ?c where {
				?a rdfs:label ?c.
				?b foaf:primaryTopic ?a.
				?a rdf:type ?e.
				?a geo:geometry ?d.
				filter STRSTARTS(LCASE(STR(?c)), \"""" + self.ambiguous_place_name + """,\").
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
			locations_db.append(result['a']['value'])
			locations_wiki.append(result['b']['value'])
			locations.append(result['c']['value'])
		self.candidate_locations = locations
		self.candidate_locations_db = locations_db
		self.candidate_locations_wiki = locations_wiki		






if __name__ == "__main__":
	short_text = """Washington, D.C., formally the District of Columbia and commonly referred to as "Washington", "the District", or simply "D.C.", is the capital of the United States."""
	TSM.named_emtity_recognition(short_text)


	# tsm = TSM("washington")	
	# tsm.get_candidate_locations()