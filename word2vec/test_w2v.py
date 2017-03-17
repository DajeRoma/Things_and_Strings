#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 15, 2017

@author: Yiting Ju
'''
import csv
import os
import sys

sys.path.append('/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/')

from wiki import wiki
from Word2VecModel import Word2VecModel

reload(sys)  
sys.setdefaultencoding('utf8')


CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TESTING_SENTENCES_FILE_PATH = os.path.join(
		os.path.dirname(CURRENT_DIR_PATH),
		"testing_data",
		"testing_sentence_city_ambiPlaceName_Mar14.csv")

W2V_TRAINED_MODEL_FOLDER_PATH = '/home/yiting/data_ThingsString'



class test_w2v():
	def __init__(self):
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		self.load_testing_data()


	def load_testing_data(self, 
						testingDataFilePath=TESTING_SENTENCES_FILE_PATH):
		listOfList = read_listOfList_from_CSV(TESTING_SENTENCES_FILE_PATH)
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		for row in listOfList:
			self.testing_sentences.append(row[0])
			self.ground_truth.append(row[1])
			self.annoted_place_names.append(row[2])


	def run_w2v_in_batch(self, result_csv_path):
		if not self.testing_sentences \
			or not self.ground_truth \
			or not self.annoted_place_names:
			print "[Error] No testing data or ground truth"
			return None
		if len(self.testing_sentences) != len(self.ground_truth) \
			or len(self.testing_sentences) != len(self.annoted_place_names):
			print "[Error] No testing data length not match"
			return None
		wk = wiki()		
		trained_model_filePath = os.path.join(W2V_TRAINED_MODEL_FOLDER_PATH,
												"glove.6B",
												"glove.6B.50d.txt")
		w2v = Word2VecModel()
		w2v.load_w2v_model(trained_model_filePath)
		for i in range(len(self.testing_sentences))[:]:
			testing_sent = self.testing_sentences[i]
			surface_form = self.annoted_place_names[i]
			candidate_places_wiki_path = wk.get_candidate_places_file_path(
											surface_form.title())
			candidate_places_count = len(candidate_places_wiki_path)
			candidate_score_dict = {}
			print "[info] Testing sentence No.", str(i+1), "..."
			print "[info]   ambiguous place name: {} ({})"\
						.format(str(surface_form), str(candidate_places_count))
			for candidate_place in candidate_places_wiki_path:
				candidate_place_wiki = wk.read_wiki_content_as_str(candidate_place)
				score = w2v.get_sents_dif_wmd(testing_sent, candidate_place_wiki)
				candidate_score_dict[path_to_place_name(candidate_place)] = score
			write_dict_to_row_csv(candidate_score_dict, result_csv_path, append=True)




def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList


def write_dict_to_row_csv(dict_to_write, csv_file_path, append=False):
	list_to_write = []
	for key in dict_to_write:
		list_to_write.append(key)
		list_to_write.append(dict_to_write[key])
	write_type = "a" if append==True else "wb" 
	with open(csv_file_path, write_type) as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
								quotechar='"', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(list_to_write)


def path_to_place_name(file_path):
	place_name = file_path[file_path.rfind('/')+1:]
	place_name = place_name[:place_name.find('.txt')]
	place_name = place_name.replace("_", " ")
	return place_name


if __name__ == '__main__':
	test_instance = test_w2v()
	result_output_path = os.path.join(CURRENT_DIR_PATH, "w2v_glove_50d_wmd_Mar16.csv")
	test_instance.run_w2v_in_batch(result_output_path)
