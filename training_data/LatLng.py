# -*- coding: utf-8 -*-

import csv
import json
import requests


# from SPARQLWrapper import SPARQLWrapper, JSON

class LatLng:
	def __init__(self):
		pass


	"""
		Return lat and lng given a place uri in DBpedia
		  place_uri -> "http://dbpedia.org/resource/Washington,_Arkansas"
	"""
	@staticmethod
	def get_lat_lng_from_DBpedia_URI(place_uri):  
		prefix = "PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>"
		query = prefix + """SELECT (str(?geom) AS ?g) (strlen(?g) AS ?len) 
							WHERE {<""" + place_uri + """> geo:geometry ?geom} 
							ORDER BY DESC(?len)"""
		parameters = {'query': query, 'format': 'json'}
		sparqlRequest = requests.get('http://dbpedia.org/sparql', params = parameters)
		# print sparqlRequest.json()
		results = sparqlRequest.json()["results"]["bindings"]
		if len(results) == 0:
			# print place_uri
			return None, None
		point_coor = results[0]['g']['value'][6:-1].split(' ')
		lat, lng = point_coor[1], point_coor[0]
		return lat, lng



"""
	wikipedia: https://en.wikipedia.org/wiki/Washington,_Arkansas
	dbpedia: http://dbpedia.org/resource/Washington,_Arkansas
"""
def wiki_url_to_db_uri(wiki_url):
	dbpedia_uri = wiki_url.replace("https://en.wikipedia.org/wiki", "http://dbpedia.org/resource")
	return dbpedia_uri


def read_listOfLists_from_CSV(csv_file_path):
	listOfLists = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfLists.append(row)
	return listOfLists


def write_listOfLists_from_CSV(listOfLists, csv_file_path):
	with open(csv_file_path, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for list_entry in listOfLists:
			spamwriter.writerow(list_entry)


def add_coor_in_batch():
	ll = LatLng()
	list_of_records = read_listOfLists_from_CSV("/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/wiki_most_common_us_place_name_double_cleaned.csv")
	list_to_return = []
	counter = 1
	for record in list_of_records:
		lat, lng = ll.get_lat_lng_from_DBpedia_URI(wiki_url_to_db_uri(record[2]))
		redirected_db_uri = wiki_url_to_db_uri(record[2])
		if not lat:
			redirected_db_uri = get_redirect_db_uri(record[2])
			if not redirected_db_uri:
				lat, lng = None, None
			else:
				lat, lng = ll.get_lat_lng_from_DBpedia_URI(redirected_db_uri)
		list_to_return.append(record + [redirected_db_uri, lat, lng])
		print counter
		counter += 1
	write_listOfLists_from_CSV(list_to_return, "/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/wiki_most_common_us_place_name_double_cleaned_coor.csv")


def get_redirect_db_uri(url):
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
		redirct_db_uri = results[0]['c']['value']
		# redirct_url = redirct_url.replace("http://dbpedia.org/resource/", "http://en.wikipedia.org/wiki/")
		print url, "\n>>", redirct_db_uri
		return redirct_db_uri
		# return get_db_entities_from_url(redirct_url)
	else:
		return None

	




if __name__ == '__main__':
	# lat, lng =  LatLng.get_lat_lng_from_DBpedia_URI("http://dbpedia.org/resource/Washington,_Arkansas")
	# print lat, lng
	# place_uri = "http://dbpedia.org/resource/Washington,_District_of_Columbia"
	# LatLng.get_lat_lng_from_DBpedia_URI(place_uri)

	# add_coor_in_batch()

	# get_redirect_db_uri("https://en.wikipedia.org/wiki/Washington,_District_of_Columbia")

<<<<<<< HEAD
	pass
=======
	pass
>>>>>>> 0d68dc1cbaa3f11855f8cf2528170e86b6ccba1b
