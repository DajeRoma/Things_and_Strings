#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 14, 2017

@author: Yiting Ju
'''

import csv
from nltk import word_tokenize
import numpy as np

# [Testing Sentence] || dover, vermont || dover
TESTING_SENTENCE_FILEPATH = "/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/testing_data/testing_sentence_city_ambiPlaceName.csv"
# Washington, District of Columbia || Washington
WIKI_MOST_COMMON_US_PLACE_NAME_MAR_14 = "/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/wiki_most_common_us_place_name_cleaned.csv"




def find_difference(source_file, target_file):
	source_cities = read_listOfList_from_CSV(source_file)
	target_cities = read_listOfList_from_CSV(target_file)
	source_cities_set = set([source_city[1].lower() for source_city in source_cities])
	target_cities_set = set([target_city[0].lower() for target_city in target_cities])
	in_source_not_in_target = source_cities_set - target_cities_set
	in_target_not_in_source = target_cities_set - source_cities_set
	print len(source_cities_set), len(target_cities_set), len(in_source_not_in_target), len(in_target_not_in_source)
	return in_source_not_in_target, in_target_not_in_source



def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList


def get_stat(list_of_lists):
	sents = []
	locations = []
	ambi_place_names = []
	for row in list_of_lists:
		sents.append(row[0])
		if row[1] not in locations:
			locations.append(row[1])
		if row[2] not in ambi_place_names:
			ambi_place_names.append(row[2])
	print len(locations), len(ambi_place_names)
	sent_length = []
	for sent in sents:
		words = word_tokenize(sent)
		sent_length.append(len(words))
	print np.mean(sent_length), np.median(sent_length)





if __name__ == '__main__':
	# in_A_not_in_B, in_B_not_in_A = find_difference(TESTING_SENTENCE_FILEPATH, WIKI_MOST_COMMON_US_PLACE_NAME_MAR_14)
	# for item in in_A_not_in_B:
	# 	print item
	# print "====="
	# for item in in_B_not_in_A:
	# 	print item

	ll = read_listOfList_from_CSV("testing_sentence_city_ambiPlaceName_Mar14.csv")	
	get_stat(ll)
