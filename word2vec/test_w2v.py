#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 15, 2017

@author: Yiting Ju
'''
import csv
import os
import sys
from operator import itemgetter

sys.path.append('/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/')

from wiki import wiki
from Word2VecModel import Word2VecModel
import numpy as np

reload(sys)  
sys.setdefaultencoding('utf8')


CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TESTING_SENTENCES_FILE_PATH = os.path.join(
		os.path.dirname(CURRENT_DIR_PATH),
		"testing_data",
		"testing_sentence_city_ambiPlaceName_Mar14.csv")

W2V_TRAINED_MODEL_FOLDER_PATH = '/home/yiting/data_ThingsString'

SCORE_METHOD = "para_wmd" 	# "wmd" "avgvec" "para_wmd"
INCREMENT_SCORE = True		# True for "wmd", "avgvec" "para_wmd"
MODEL_SOURCE = "google_news"		# "glove" "google_news"
DIMENSION = "300d"
RESULT_OUTPUT_NAME = "w2v_" + MODEL_SOURCE + "_" + DIMENSION + "_" + SCORE_METHOD + "_Mar16.csv"
if MODEL_SOURCE == "glove":
	TRAINED_MODEL_FILE = "glove.6B/glove.6B." + DIMENSION + ".txt"
elif MODEL_SOURCE == "google_news":
	TRAINED_MODEL_FILE = "GoogleNews-vectors-negative300.bin"
# elif MODEL_SOURCE == "glove":
	# TRAINED_MODEL_FILE = "glove.6B/glove.6B.50d.txt"





class test_w2v():
	def __init__(self):
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		self.load_testing_data()
		self.result = []


	def load_testing_data(self, 
						testingDataFilePath=TESTING_SENTENCES_FILE_PATH):
		listOfList = read_listOfList_from_CSV(testingDataFilePath)
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		for row in listOfList:
			self.testing_sentences.append(row[0])
			self.ground_truth.append(row[1])
			self.annoted_place_names.append(row[2])

	"""
		score_method: "wmd" or "avgvec"
	"""
	def run_w2v_in_batch(self, result_csv_path, score_method):
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
												TRAINED_MODEL_FILE)
		w2v = Word2VecModel()
		if MODEL_SOURCE == "glove":
			w2v.load_w2v_model(trained_model_filePath)
		else:
			w2v.load_w2v_model(trained_model_filePath, binary=True)
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
				score = 0
				if score_method == "wmd":
					score = w2v.get_sents_dif_wmd(testing_sent, candidate_place_wiki)
				elif score_method == "avgvec":
					score = w2v.get_sents_similarity_avgvec(testing_sent, candidate_place_wiki)
				elif score_method == "para_wmd":
					score = w2v.get_paragraphs_dif_wmd(candidate_place_wiki, testing_sent)
				else:
					print "[error] score_method is set not correctly"
				candidate_score_dict[path_to_place_name(candidate_place)] = score
			write_dict_to_row_csv(candidate_score_dict, result_csv_path, append=True)


	def load_result_data(self, result_file_path, reverse_option=True):
		raw_result = read_listOfList_from_CSV(result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)/2):
				result_for_a_sentence.append((row[2*i].lower(), row[2*i+1]))
			if "wmd" in SCORE_METHOD:
				result_for_a_sentence = standardize_wmd(result_for_a_sentence)
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=reverse_option)
			result_list.append(sorted_result)
		self.result = result_list


	def evaluate(self, limit):
		if len(self.ground_truth) != len(self.result):
			print "[Warning] Lenth of the ground truth and the result do not match"
			print "testing/ground truth:", len(self.result), len(self.ground_truth) 
		if limit > len(self.result) and limit <= 0:
			print "[Error] Limit set out of range"
			return
		tp, p_hat, p = 0, 0, 0
		rank_list = []
		for i in xrange(min(len(self.ground_truth), len(self.result))):
			p += 1
			result_for_a_sentence = self.result[i]
			for j in xrange(limit):
				p_hat += 1
				if str(result_for_a_sentence[j][0]) == str(self.ground_truth[i]):
					tp += 1
					rank_list.append(j+1)
		precision = 1.0 * tp / p_hat
		recall = 1.0 * tp / p
		f_score = 2.0 * (precision * recall) / (precision + recall)
		reciprocal_rank_sum = 0
		for rank in rank_list:
			if rank > 0:
				reciprocal_rank_sum += 1.0 / rank
		mean_reciprocal_rank = 1.0 * reciprocal_rank_sum / p
		# print "tp:",tp , "\tp-hat:", p_hat, "\tp:", p
		# print "F Score:", f_score
		# print "MRR:", mean_reciprocal_rank
		# print "precision:", precision
		# print "Recall:", recall
		print str(tp) + "\t" + str(p_hat) + "\t" + str(p) + "\t" + str(f_score) + "\t" + str(mean_reciprocal_rank) + "\t" + str(precision) + "\t" + str(recall)
		# return f_score, mean_reciprocal_rank, precision, recall


	def evaluate_percentile(self, percentile):
		if len(self.ground_truth) != len(self.result):
			print "[Warning] Lenth of the ground truth and the result do not match"
			print "testing/ground truth:", len(self.result), len(self.ground_truth) 
		percentile = int(percentile)
		if percentile < 0:
			print "[Error] percentile should be a non-negative integer"
			return
		tp, p_hat, p = 0, 0, 0
		rank_list = []
		for i in xrange(min(len(self.ground_truth), len(self.result))):
		# for i in [334]:
			p += 1
			result_for_a_sentence = self.result[i]
			result_for_a_sentence = filter_by_percentile(result_for_a_sentence, percentile)
			for j in xrange(len(result_for_a_sentence)):
				p_hat += 1
				if str(result_for_a_sentence[j][0]) == str(self.ground_truth[i]):
					tp += 1
					rank_list.append(j+1)
		precision = 1.0 * tp / p_hat
		recall = 1.0 * tp / p
		f_score = 2.0 * (precision * recall) / (precision + recall)
		reciprocal_rank_sum = 0
		for rank in rank_list:
			if rank > 0:
				reciprocal_rank_sum += 1.0 / rank
		mean_reciprocal_rank = 1.0 * reciprocal_rank_sum / p
		# print "tp:",tp , "\tp-hat:", p_hat, "\tp:", p
		# print "F Score:", f_score
		# print "MRR:", mean_reciprocal_rank
		# print "precision:", precision
		# print "Recall:", recall
		print str(tp) + "\t" + str(p_hat) + "\t" + str(p) + "\t" + str(f_score) + "\t" + str(mean_reciprocal_rank) + "\t" + str(precision) + "\t" + str(recall)
		# return f_score, mean_reciprocal_rank, precision, recall


"""
	standardize the wmd score; also reverse the ordering, making it 
	  the higher the score, the more similar
"""
def standardize_wmd(wmd_tuples):
	cities = []
	distances = []
	for wmd_tuple in wmd_tuples:
		cities.append(wmd_tuple[0])
		distances.append(float(wmd_tuple[1]))
	mean = np.mean(distances)
	std = np.std(distances)
	standardized_distances = []
	for i in xrange(len(distances)):
		if std == 0:
			standardized_distances.append((cities[i] , "0"))
		else:
			standardized_distances.append((cities[i] , str((distances[i]) - mean / std)))
	return standardized_distances


"""
	Given a list of scores, calculate the percentile, and return 
	  the part of the list of scores that is higher than the percentile
	Note: percent goes from 1 ~ 100
"""
def filter_by_percentile(city_scores, percent):
	scores = []
	for city_score in city_scores:
		scores.append(float(city_score[1]))
	limit = np.percentile(scores, percent)
	new_city_scores = []
	for city_score in city_scores:
		# floating issue causes incorrect comparison
		if round(float(city_score[1]), 8) >= round(float(limit), 8):
			new_city_scores.append(city_score)
	return new_city_scores


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
	result_output_path = os.path.join(CURRENT_DIR_PATH, RESULT_OUTPUT_NAME)
	
	# 1. Run the model and get the result
	# test_instance.run_w2v_in_batch(result_output_path, SCORE_METHOD)

	# 2. Evaluate the result
	# test_instance.load_result_data(result_output_path, reverse_option=INCREMENT_SCORE)
	# for i in xrange(1):
	# 	test_instance.evaluate(i+1)

	test_instance.load_result_data(result_output_path, reverse_option=INCREMENT_SCORE)
	for i in xrange(0, 101, 5):
		test_instance.evaluate_percentile(i)