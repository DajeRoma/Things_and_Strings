# -*- coding: utf-8 -*-

import csv
import codecs
import sys
import os
import requests
from subprocess import Popen
from nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger

import wiki
import util
from EntityCooccurrence import EntityCooccurrence
from EntityCooccurrence import get_wiki_entities_from_url
from Word2VecModel import Word2VecModel

reload(sys)  
sys.setdefaultencoding('utf8')

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CANDIDATES_LIST_PATH = os.path.join(CURRENT_DIR_PATH, "candidate_locations_list.csv")
WIKI_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "wikipedia")
WIKI_ENTITIES_PATH = os.path.join(CURRENT_DIR_PATH, "wikipedia_entities.csv")
DB_ENTITIES_PATH = os.path.join(CURRENT_DIR_PATH, "dbpedia_entities.csv")
LDA_RESULT_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "lda_result")
FULLER7_DIR_PATH = "/home/yiting/javaWorkspace/LDA/files/"
GOOGLE_NEW_WE_TRAINED_MODEL_PATH = os.path.join("/home/yiting/data_ThingsString",
										"GoogleNews-vectors-negative300.bin")


class TSM:
	def __init__(self, place_name, sentence):
		self.sentence = sentence
		self.ambiguous_place_name = place_name.lower()	# boston
		self.candidate_locations = []	# ['Boston, Davao Oriental',
		self.candidate_locations_db = []
		self.candidate_locations_wiki = [] 
		# ['http://en.wikipedia.org/wiki/Boston,_Davao_Oriental', ...]
		self.candidate_locations_long = []
		self.candidate_locations_lat = []
		self.candidate_locations_wiki_content = []

		self.new_ambiguous_name = False
		self.all_ambiguous_names_list = set()
		self.all_candidates = {}
		if place_name:
			self.load_existing_list()
			self.get_candidate_locations()
			self.load_wiki_content()
			self.write_to_candidate_location_list()

		self.w2v = Word2VecModel()
		self._preload_w2v()

		self.all_candidate_locations_wiki_entities = {}
		self.all_candidate_locations_db_entities = {}

		self.ec_result = {}
		# {'boston, davao oriental': 0.9310071285130486, 
		# 'boston, culpeper county, virginia': 0.9310071285130486, 
		# 'boston, georgia': 0.9310071285130486, 
		# 'boston, belize': 0.9310071285130486, 
		# 'boston': 3.6390573296152584, 
		# 'boston, county clare': 0.9310071285130486}
		self.lda_result = {}
		# {'boston, davao oriental': 0.6, 
		# 'boston, culpeper county, virginia': 0.44965480638636757, 
		# 'boston, georgia': 0.497400847366547, 
		# 'boston, belize': 0.6, 
		# 'boston': 0.5232323047852842, 
		# 'boston, county clare': 0.6}
		self.we_result = {}
		# {'boston, davao oriental': 3.0747995519965303, 
			# 'boston, culpeper county, virginia': 3.143116787634168, 
			# 'boston, georgia': 2.884906165268664, 
			# 'boston, belize': 2.951150195973547, 
			# 'boston, indiana': 2.5267059528895324,
			# 'boston, pennsylvania': 2.965466758122623, 
			# 'boston': 2.1757625944288757, 
			# 'boston, county clare': 2.9921878306078407}

		self.ec_nor_result = {}
		self.lda_nor_result = {}
		self.we_nor_result = {}

		self.integrated_result = []


	def new_query(self, place_name, sentence):
		self.sentence = sentence
		self.ambiguous_place_name = place_name.lower()	# boston
		self.candidate_locations = []	# ['Boston, Davao Oriental',
		self.candidate_locations_db = []
		self.candidate_locations_wiki = [] 
		# ['http://en.wikipedia.org/wiki/Boston,_Davao_Oriental', ...]
		self.candidate_locations_long = []
		self.candidate_locations_lat = []
		self.candidate_locations_wiki_content = []

		self.new_ambiguous_name = False
		self.all_ambiguous_names_list = set()
		self.all_candidates = {}
		self.load_existing_list()
		self.get_candidate_locations()
		self.load_wiki_content()
		self.write_to_candidate_location_list()

		# no need to reload
		# self.w2v = Word2VecModel()
		# self._preload_w2v()

		self.all_candidate_locations_wiki_entities = {}
		self.all_candidate_locations_db_entities = {}

		self.ec_result = {}
		self.lda_result = {}
		self.we_result = {}

		self.ec_nor_result = {}
		self.lda_nor_result = {}
		self.we_nor_result = {}

		self.integrated_result = []



	def call_integration_model(self):
		self.call_entity_cooccurrence()
		self.call_topic_model()
		self.call_word_embedding_model()

		self._normalize_result()
		self._integrate(0.31, 0.22, 0.47)
		print self.integrated_result
		return self.integrated_result


	def _integrate(self, ec_weight, lda_weight, we_weight):
		self.integrated_result = {}
		for city_name in self.ec_nor_result:
			self.integrated_result[city_name] = self.ec_nor_result[city_name] * ec_weight \
											+ self.lda_nor_result[city_name] * lda_weight \
											+ self.we_nor_result[city_name] * we_weight


	"""
		Normalize the results of all three models
	"""
	def _normalize_result(self):
		self.ec_nor_result = TSM._normalize_result_list(self.ec_result)
		self.lda_nor_result = TSM._normalize_result_list(self.lda_result, reverse = True)
		self.we_nor_result = TSM._normalize_result_list(self.we_result, reverse = True)


	"""
		Normalize the scores between 0 and 1 in the result_dict
	  	note: result_dict = {"city1": "0.05", "city2": "0.04", ... }
	"""
	@staticmethod
	def _normalize_result_list(result_dict, reverse = False):	
		nor_result_dict = {}		
		scores = []
		for city_name in result_dict:
			scores.append(float(result_dict[city_name]))
		maximum = max(scores)
		minimum = min(scores)
		for city_name in result_dict:
			if maximum - minimum == 0:
				nor_result_dict[city_name] = 0.5
			else:
				if reverse:
					nor_result_dict[city_name] = (maximum - float(result_dict[city_name])) / (maximum - minimum)
				else:
					nor_result_dict[city_name] = (float(result_dict[city_name]) - minimum) / (maximum - minimum)
		return nor_result_dict


	def _preload_w2v(self):
		self.w2v.load_w2v_model(GOOGLE_NEW_WE_TRAINED_MODEL_PATH, binary=True)


	def call_word_embedding_model(self):		
		for i in xrange(len(self.candidate_locations)):
			candidate_name = self.candidate_locations[i]
			candidate_wiki_content = self.candidate_locations_wiki_content[i]
			candidate_we_score = self.w2v.get_paragraphs_dif_wmd(candidate_wiki_content, self.sentence)
			self.we_result[candidate_name.lower()] = candidate_we_score
		print self.we_result


	def call_topic_model(self):
		lda_result_file_path = os.path.join(LDA_RESULT_DIR_PATH, "temp.csv")
		self._call_lda_jar(lda_result_file_path)
		self._read_lda_result(lda_result_file_path)
		print self.lda_result


	def _read_lda_result(self, lda_result_file_path):
		with open(lda_result_file_path, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
			for row in spamreader:
				self.lda_result[row[0]] = float(row[1])


	def _call_lda_jar(self, lda_result_file_path):
		lda_result = lda_result_file_path
		command = "java -jar topic.jar \"" + self.ambiguous_place_name + "\" \"" + self.sentence \
		 			+ "\" \"" + CANDIDATES_LIST_PATH + "\" \"" + FULLER7_DIR_PATH + "\" \"" \
		 			+ lda_result + "\""
		print "Calling", command
		try:
			e = Popen(
				command,
				cwd = CURRENT_DIR_PATH,
				shell = True
			)
			stdout, stderr = e.communicate()
		except IOError as (errno,strerror):
			print "I/O error({0}): {1}".format(errno, strerror)


	def call_entity_cooccurrence(self):
		ec = EntityCooccurrence()
		for ambi_name in self.all_candidates:
			ec.ambi_name_to_candidates[ambi_name.lower()] = \
				[item.lower() for item in self.all_candidates[ambi_name].keys()]
		ec.load_wiki_entities(WIKI_ENTITIES_PATH)
		ec.load_dbpedia_entities(DB_ENTITIES_PATH)

		if self.new_ambiguous_name is True:
			self._add_entities_for_ec(ec)
		self.ec_result = ec.apply_model(self.sentence, self.ambiguous_place_name)
		print self.ec_result


	def _add_entities_for_ec(self, ec_model):
		for i in xrange(len(self.candidate_locations)):
			db_entities = self.get_db_entities_from_url(self.candidate_locations_db[i])
			self._add_entities_to_csv(self.candidate_locations[i],
											db_entities,
											DB_ENTITIES_PATH)
			db_entities = set(db_entities)
			ec_model.candidate_db_entities[self.candidate_locations[i]] = db_entities
			wiki_entities = get_wiki_entities_from_url(self.candidate_locations_wiki[i])
			self._add_entities_to_csv(self.candidate_locations[i],
											wiki_entities,
											WIKI_ENTITIES_PATH)
			ec_model.candidate_wiki_entities[self.candidate_locations[i]] = wiki_entities
			

	@staticmethod
	def _add_entities_to_csv(location_name, entities, csvFilePath):
		with open(csvFilePath, 'a') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow([location_name] + entities)


	"""
		Given an url of a candidate place's DBpedia page url, find all entities
	"""
	@staticmethod
	def get_db_entities_from_url(url):
		entities = set()
		query = """select distinct ?b ?c
					{
					  {
						select ?b ?c
						where {
							   <""" + url + """> ?b ?c.
							   FILTER(STRSTARTS(STR(?b), "http://dbpedia.org/ontology/") || STRSTARTS(STR(?b), "http://dbpedia.org/property/")).
							   FILTER(!isLiteral(?c)).
						}
					  }
					  union
					  {
						select ?c ?b
						where {
							   ?c ?b <""" + url + """>.
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
		return list(set(entities))


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
		else:
			print "!!!!"
			os.makedirs(os.path.join(WIKI_DIR_PATH, self.ambiguous_place_name))
			print "Downloading Wikipedia text..."
			wiki.write_cities_wikis_to_disk(self.candidate_locations, 
									[self.ambiguous_place_name] * len(self.candidate_locations),
									parent_dir=WIKI_DIR_PATH)
			print "Wikipedia texts have been downloaded..."
		self._load_wiki_content_from_file()
		print "Wikipedia texts have been loaded..."


	def _load_wiki_content_from_file(self):
		for candidate_location in self.candidate_locations:
			candidate_location_file_path = os.path.join(WIKI_DIR_PATH,
												self.ambiguous_place_name,
												candidate_location.replace(" ", "_") + ".txt")
			wiki_content = self._read_from_txt_to_str(candidate_location_file_path)
			self.candidate_locations_wiki_content.append(wiki_content)


	"""
	Read text from a file and return with a string
	"""
	@staticmethod
	def _read_from_txt_to_str(txt_file_path):
		with codecs.open(txt_file_path, 'rb', encoding='utf8') as outfile:
			line_list = outfile.readlines()
		line_list = [line.strip() for line in line_list]
		# print len(line_list)
		return "\n".join(line_list).strip()


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
			print self.ambiguous_place_name, "is NOT a new ambiguous place name"
			print "Candidate locations loaded"
			return
		self.new_ambiguous_name = True
		print self.ambiguous_place_name, "is a new ambiguous place name"
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


	tsm = TSM("boston", "I went to Boston and visited harvard this morning.")
	# tsm.call_entity_cooccurrence()

	# tsm = TSM("washington", "records show 374 persons living in town in 1900. recurrent attempts to move the county seat to hope finally succeeded in 1938-39. the washington telegraph founded in 1840, and the only  newspaper published throughout the civil war, printed its last issue in 1947.")	
	# tsm.call_topic_model()
	# tsm.get_candidate_locations()
	# tsm.load_wiki_content()
	# tsm.get_candidate_locations()

	# tsm.call_word_embedding_model()

	tsm.call_integration_model()
	tsm.new_query("washington", "records show 374 persons living in town in 1900. recurrent attempts to move the county seat to hope finally succeeded in 1938-39. the washington telegraph founded in 1840, and the only  newspaper published throughout the civil war, printed its last issue in 1947.")
	tsm.call_integration_model()