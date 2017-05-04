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
		if len(results) != 1:
			print place_uri
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
		list_to_return.append(record + [lat, lng])
		print counter
		counter += 1
	write_listOfLists_from_CSV(list_to_return, "/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/wiki_most_common_us_place_name_double_cleaned_coor.csv")



if __name__ == '__main__':
	# lat, lng =  LatLng.get_lat_lng_from_DBpedia_URI("http://dbpedia.org/resource/Washington,_Arkansas")
	# print lat, lng
	# add_coor_in_batch()
	pass