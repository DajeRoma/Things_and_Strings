# -*- coding: utf-8 -*-
import csv
import sys
import os
import requests
import json
from operator import itemgetter

reload(sys)  
sys.setdefaultencoding('utf8')

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

DBPEDIA_SPOTLIGHT_URL = "http://stko-lod.geog.ucsb.edu:2222"


class DBpedia_Spotlight():
	def __init__(self):
		self.dbsl_url = DBPEDIA_SPOTLIGHT_URL + "/rest/"

	def candidates(self, text, place_name):
		place_score_list = []
		place_list = []
		url = self.dbsl_url + "candidates?text=" + text + "&confidence=0.2&support=0&types=place";
		headers = {"Accept": "application/json"}
		response = requests.get(url, headers=headers)
		res_json = response.json()
		print res_json
		if "surfaceForm" not in res_json["annotation"]:
			return []
		if isinstance(res_json["annotation"]["surfaceForm"], list):
			for surfaceform in res_json["annotation"]["surfaceForm"]:
				surface_form = surfaceform["@name"].lower()
				if place_name.lower() in surface_form:
					if isinstance(surfaceform["resource"], list):
						for res in surfaceform["resource"]:
							place = (res["@label"].replace('_', '').lower() , float(res["@finalScore"]))
							if place not in place_list:
								place_list.append(place[0])
								place_score_list.append(place)
					else:
						place = (surfaceform["resource"]["@label"].replace('_', '').lower() , float(surfaceform["resource"]["@finalScore"]))
						if place not in place_list:
							place_list.append(place[0])
							place_score_list.append(place)
		else:
			surface_form = res_json["annotation"]["surfaceForm"]["@name"].lower()
			surfaceform = res_json["annotation"]["surfaceForm"]
			if place_name.lower() in surface_form:
				if isinstance(surfaceform["resource"], list):
					for res in surfaceform["resource"]:
						place = (res["@label"].replace('_', '').lower() , float(res["@finalScore"]))
						if place not in place_list:
							place_list.append(place[0])
							place_score_list.append(place)
				else:
					place = (surfaceform["resource"]["@label"].replace('_', '').lower() , float(surfaceform["resource"]["@finalScore"]))
					if place not in place_list:
						place_list.append(place[0])
						place_score_list.append(place)
		place_score_list_sorted = sorted(place_score_list, key=itemgetter(1), reverse=True)
		place_list_sorted = []
		for place_score in place_score_list_sorted:
			place_list_sorted.append(place_score)
		return place_list_sorted

if __name__ == "__main__":
	dbsl = DBpedia_Spotlight()
	print dbsl.candidates("I am living in Springfield", "springfield")