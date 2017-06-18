# -*- coding: utf-8 -*-
import csv
import requests
import json

STATES_LIST = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']


class OpenCalais():
	def __init__(self):
		self.url = "https://api.thomsonreuters.com/permid/calais"
		self.headers = {"Content-Type": "text/raw", 
					"Accept": "application/json",
					"x-ag-access-token": "5CSCGy1jw4x7vY0FtLERrHZHDaRwynKq",
					"outputFormat": "application/json"}
# 5CSCGy1jw4x7vY0FtLERrHZHDaRwynKq
# o0fgGOQ7cCYZCKiXJ4U5O78CIjQdDbRS

	def annotate(self, text, place_name):
		res = requests.post(self.url, data = text, headers = self.headers)
		if res.status_code != 200:
			return []
		res_json = json.loads(res.text)
		place_entities = self.parse(res_json, place_name)
		return place_entities


	def parse(self, json_result, place_name):
		extracted_entities = []
		for key in json_result:
			if "SocialTag" in key:
				social_tag = json_result[key]
				if "name" in social_tag and \
					place_name in social_tag["name"].lower():
					extracted_entities.append(social_tag["name"].lower())
				if "name" in social_tag and \
					social_tag["name"].lower() in STATES_LIST:
					extracted_entities.append(place_name + ", " + social_tag["name"].lower())
			if "genericHasher" in key:
				ner_tag = json_result[key]
				if "resolutions" in ner_tag:
					for item in ner_tag["resolutions"]:
						if place_name in item["name"].lower():
							resolution_res = item["name"].lower()
							if "washington" in resolution_res and \
								item["latitude"] == "38.89" and \
								item["longitude"] == "-77.03":
								extracted_entities.append("washington, district of columbia")
							if "united states" in resolution_res:
								resolution_res = resolution_res[:resolution_res.find("united states") - 1].strip()
								extracted_entities.append(resolution_res)
		return list(set(extracted_entities))



if __name__ == "__main__":
   oc = OpenCalais()
   print oc.annotate("Washington, DC, the U.S. capital, is a compact city on the Potomac River, bordering the states of Maryland and Virginia.", "washington")
