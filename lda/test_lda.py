#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on March 5, 2017

@author: Yiting Ju
'''
import csv
import os
import sys
from operator import itemgetter

# sys.path.append('/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/')

# from wiki import wiki
import numpy as np

reload(sys)  
sys.setdefaultencoding('utf8')


CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TESTING_SENTENCES_FILE_PATH = os.path.join(
		os.path.dirname(CURRENT_DIR_PATH),
		"testing_data",
		"testing_sentence_city_ambiPlaceName_Mar14.csv")



class test_lda():
	def __init__(self):
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		self._load_testing_data()
		self.result = []


	"""
		Load testing data:
		  1. testing sentences
		  2. result (actual place name entity)
		  3. surface form (ambiguous place name)
	"""
	def _load_testing_data(self, 
						testing_data_file_path = TESTING_SENTENCES_FILE_PATH):
		listOfList = read_listOfLists_from_CSV(testing_data_file_path)
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		for row in listOfList:
			self.testing_sentences.append(row[0])
			self.ground_truth.append(row[1])
			self.annoted_place_names.append(row[2])


	def run_lda_in_batch(self, result_csv_path):
		pass


	def load_result_data(self, result_csv_path):
		raw_result = read_listOfLists_from_CSV(result_csv_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange((len(row)+1)/2):
				result_for_a_sentence.append((row[2*i].lower(), float(row[2*i+1])))
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=True)
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


def read_listOfLists_from_CSV(csv_file_path):
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
	test_instance = test_lda()
	result_output_name = "lda_testing_result_May5.csv"
	result_output_path = os.path.join(CURRENT_DIR_PATH, result_output_name)
	

	# Evaluate the result
	# test_instance.load_result_data(result_output_path)
	# for i in xrange(2):
	# 	test_instance.evaluate(i+1)

	test_instance.load_result_data(result_output_path)
	for i in xrange(0, 101):
		test_instance.evaluate_percentile(i)