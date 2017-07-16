# -*- coding: utf-8 -*-

import csv
import codecs
import sys
import requests
from nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger


reload(sys)  
sys.setdefaultencoding('utf8')


class TSM:
	def __init__(self, place_name):
		self.ambiguous_place_name = place_name.lower()

	def named_emtity_recognition(self):
		classifier = './english.all.3class.distsim.crf.ser.gz'
		jar = './stanford-ner.jar'
		tagger = StanfordNERTagger(classifier, jar)
		 
		sentence = word_tokenize("Rami Eid is studying at Stony Brook University in NY")
		 
		print tagger.tag(sentence)


	def get_candidate_locations(self):
		entities = set()

		query = """select distinct ?a, ?b where {
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
		print sparqlRequest.json()
		results = sparqlRequest.json()["results"]["bindings"]
		# in case "redirected"
		# if len(results) == 1 and results[0]['b']['value'] == "http://dbpedia.org/ontology/wikiPageRedirects":
		# 	redirct_url = results[0]['c']['value']
		# 	redirct_url = redirct_url.replace("http://dbpedia.org/resource/", "http://en.wikipedia.org/wiki/")
		# 	return get_db_entities_from_url(redirct_url)
		# for result in results:
		# 	obj = result['c']['value']
		# 	if "http://dbpedia.org/resource/" in obj:
		# 		entity = obj[len("http://dbpedia.org/resource/"):]
		# 		entity = entity.replace('_', " ")
		# 		if '(' in entity:
		# 			entity = entity[:entity.find('(')]
		# 		entity = entity.strip()
		# 		entities.add(entity)
		# 		# print entity
		# return list(entities)






if __name__ == "__main__":
	tsm = TSM("washington")
	tsm.get_candidate_locations()