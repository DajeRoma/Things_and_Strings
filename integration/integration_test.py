# -*- coding: utf-8 -*-
import csv
import sys
import os
import numpy as np
from operator import itemgetter
from multiprocessing import Pool

sys.path.append('/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/')
from entity_cooccurrence.EntityCooccurrence import EntityCooccurrence
from word2vec.Word2VecModel import Word2VecModel

reload(sys)  
sys.setdefaultencoding('utf8')

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CANDIDATES_LIST_CSV_FILE_PATH = os.path.join(
									os.path.dirname(CURRENT_DIR_PATH), 
									"training_data",
									"wiki_most_common_us_place_name_double_cleaned.csv")
TESTING_SENTENCES_FILE_PATH = os.path.join(
			os.path.dirname(CURRENT_DIR_PATH),
			"testing_data",
			"testing_sentence_city_ambiPlaceName_Mar14.csv")
DEFAULT_RESULT_PATH = os.path.join(
					CURRENT_DIR_PATH,
					"comprehensive_summary_May24.csv")


class integration_test:
	def __init__(self):
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		self._load_testing_data()
		self.ec_result = []
		self.lda_result = []
		self.w2v_result = []
		self.ec_std_result = []
		self.lda_std_result = []
		self.w2v_std_result = []
		self.integrated_result = []


	"""
		Load testing data:
		  1. testing sentences
		  2. result (actual place name entity)
		  3. surface form (ambiguous place name)
	"""
	def _load_testing_data(self, 
						testing_data_file_path = TESTING_SENTENCES_FILE_PATH):
		listOfLists = read_listOfLists_from_CSV(testing_data_file_path)
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		for row in listOfLists:
			self.testing_sentences.append(row[0])
			self.ground_truth.append(row[1])
			self.annoted_place_names.append(row[2])


	"""
		load result from three models
		  ec_res, lda_res, w2v_res are paths to the files
	"""
	def load_all_three_result(self, ec_res, lda_res, w2v_res):
		self.load_ec_result(ec_res)
		self.load_lda_result(lda_res)
		self.load_w2v_result(w2v_res)


	def load_ec_result(self, ec_result_file_path):
		raw_result = read_listOfLists_from_CSV(ec_result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)/2):
				result_for_a_sentence.append((row[2*i].lower(), row[2*i+1]))
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=True)
			result_list.append(sorted_result)
		self.ec_result = result_list


	def load_lda_result(self, lda_result_file_path):
		raw_result = read_listOfLists_from_CSV(lda_result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)/2):
				result_for_a_sentence.append((row[2*i].lower(), row[2*i+1]))
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=False)
			result_list.append(sorted_result)
		self.lda_result = result_list


	"""
		note: the result form w2v is not nessarily the larger the value, the better
	"""
	def load_w2v_result(self, w2v_result_file_path, reverse_option=True):
		raw_result = read_listOfLists_from_CSV(w2v_result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)/2):
				result_for_a_sentence.append((row[2*i].lower(), row[2*i+1]))
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=reverse_option)
			result_list.append(sorted_result)
		self.w2v_result = result_list


	"""
		Standardize the results of all three models
	"""
	def standarid_result(self):
		self.ec_std_result = standardize_result_list(self.ec_result)
		# self.ec_std_result = self.ec_result
		self.lda_std_result = standardize_result_list(self.lda_result, reverse = True)
		self.w2v_std_result = standardize_result_list(self.w2v_result, reverse = True)


	def integrate(self, ec_weight, lda_weight, w2v_weight):
		if len(self.ground_truth) != len(self.ec_std_result):
			print "[error] Lenth of EC std result and the ground truth do not match"
			print "testing/ground truth:", len(self.ec_std_result), len(self.ground_truth)
			return
		if len(self.ground_truth) != len(self.lda_std_result):
			print "[error] Lenth of LDA std result and the ground truth do not match"
			print "testing/ground truth:", len(self.lda_std_result), len(self.ground_truth)
			return
		if len(self.ground_truth) != len(self.w2v_std_result):
			print "[error] Lenth of W2V std result and the ground truth do not match"
			print "testing/ground truth:", len(self.w2v_std_result), len(self.ground_truth)
			return
		if ec_weight < 0 or lda_weight < 0 or w2v_weight < 0 or \
			ec_weight > 1 or lda_weight > 1 or w2v_weight > 1:
			print "[error] weight should be within the range of [0, 1]"
			return
		if ec_weight + lda_weight + w2v_weight != 1:
			print "[error] sum of three weights should be 1"
			return
		self.integrated_result = []
		for i in xrange(len(self.ground_truth)):
			integrated_record = sum_3_tuple_lists_wWeights(
									self.ec_std_result[i], self.lda_std_result[i], self.w2v_std_result[i],
									ec_weight, lda_weight, w2v_weight)
			integrated_record = sorted(integrated_record, key=itemgetter(1), reverse=True)
			self.integrated_result.append(integrated_record)


	"""
		Get the testing result.
		  Percentile will be used to determine which results will be accepted
		  percentile goes from 1 ~ 100
	"""
	def evaluate_percentile(self, percentile):
		if len(self.ground_truth) != len(self.integrated_result):
			print "[Warning] Lenth of integrated model's result and the ground truth do not match"
			print "testing/ground truth:", len(self.integrated_result), len(self.ground_truth)
		percentile = int(percentile)
		if percentile < 0 or percentile > 100:
			print "[Error] percentile should be a non-negative integer lower than 101"
			return
		tp, p_hat, p = 0, 0, 0
		rank_list = []
		for i in xrange(min(len(self.ground_truth), len(self.integrated_result))):
			p += 1
			result_for_a_sentence = self.integrated_result[i]
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

		print str(tp) + "\t" + str(p_hat) + "\t" + str(p) + "\t" + str(f_score) + "\t" + str(mean_reciprocal_rank) + "\t" + str(precision) + "\t" + str(recall)


	def evaluate_percentile_best_return(self, weight1, weight2, weight3):
		if len(self.ground_truth) != len(self.integrated_result):
			print "[Warning] Lenth of integrated model's result and the ground truth do not match"
			print "testing/ground truth:", len(self.integrated_result), len(self.ground_truth)
		f_summary_dict = {}
		for k in xrange(0, 101, 1):
			percentile = int(k)			
			tp, p_hat, p = 0, 0, 0
			rank_list = []
			for i in xrange(min(len(self.ground_truth), len(self.integrated_result))):
				p += 1
				result_for_a_sentence = self.integrated_result[i]
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
			# if f_score in f_summary_dict:
			# 	print f_summary_dict[f_score]
			row_to_write = str(weight1) + "\t" + str(weight2) + "\t" + str(weight3) + "\t" + str(k) + "th" + "\t" + str(tp) + "\t" + str(p_hat) + "\t" + str(p) + "\t" + str(f_score) + "\t" + str(mean_reciprocal_rank) + "\t" + str(precision) + "\t" + str(recall)
			append_row_to_CSV(row_to_write, DEFAULT_RESULT_PATH)
			f_summary_dict[f_score] = str(weight1) + "\t" + str(weight2) + "\t" + str(weight3) + "\t" + str(k) + "th" + "\t" + str(tp) + "\t" + str(p_hat) + "\t" + str(p) + "\t" + str(f_score) + "\t" + str(mean_reciprocal_rank) + "\t" + str(precision) + "\t" + str(recall)
			# print str(tp) + "\t" + str(p_hat) + "\t" + str(p) + "\t" + str(f_score) + "\t" + str(mean_reciprocal_rank) + "\t" + str(precision) + "\t" + str(recall)
		max_f = max(f_summary_dict.keys())
		print f_summary_dict[max_f]





def sum_3_tuple_lists_wWeights(tuple_list1, tuple_list2, tuple_list3,
								weight1, weight2, weight3):
	dict1, dict2, dict3 = {}, {}, {}
	for cell in tuple_list1:
		dict1[cell[0]] = cell[1]
	for cell in tuple_list2:
		dict2[cell[0]] = cell[1]
	for cell in tuple_list3:
		dict3[cell[0]] = cell[1]
	sum_tuple_list = []
	for key in dict1.keys():
		cell = (key, float(dict1[key]) * float(weight1) + float(dict2[key]) * float(weight2) + float(dict3[key]) * float(weight3))
		sum_tuple_list.append(cell)
	return sum_tuple_list


"""
	standardize the scores in the result_list
	  note: result_list = [[("city1", "0.05"), ("city2", "0.04"), (), ...], [], ...]
"""
def standardize_result_list(result_list, reverse = False):	
	std_result_list = []
	for record in result_list:
		std_record = []
		scores = []
		for cell in record:
			scores.append(float(cell[1]))
		mean = np.mean(scores)
		std = np.std(scores)
		for cell in record:
			if std == 0:
				std_record.append((cell[0], 0))
			else:
				if reverse:
					std_record.append((cell[0], (mean - float(cell[1])) / std))
				else:
					std_record.append((cell[0], (float(cell[1]) - mean) / std))
		std_result_list.append(std_record)
	return std_result_list


def read_listOfLists_from_CSV(csv_file_path):
	listOfLists = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfLists.append(row)
	return listOfLists


def append_row_to_CSV(row, csv_file_path):
	row_to_write = row.split("\t")
	with open(csv_file_path, 'a') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(row_to_write)


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


def try_pool(i):
	sample_ec_result_file = os.path.join(CURRENT_DIR_PATH, "ec_test_result.csv")
	sample_lda_result_file = os.path.join(CURRENT_DIR_PATH, "lda_testing_result_May5.csv")
	sample_w2v_result_file = os.path.join(CURRENT_DIR_PATH, "w2v_google_news_300d_para_wmd_Mar16.csv")
	it = integration_test()
	it.load_all_three_result(sample_ec_result_file, sample_lda_result_file, sample_w2v_result_file)
	it.standarid_result()

	j = 0
	while i + j <= 100:
		weight1 = i / 100.0
		weight2 = j / 100.0
		weight3 = (100 - i - j) / 100.0
		it.integrate(weight1, weight2, weight3)
		it.evaluate_percentile_best_return(weight1, weight2, weight3)
		j += 1



if __name__ == "__main__":
	# sample_ec_result_file = os.path.join(CURRENT_DIR_PATH, "ec_test_result.csv")
	# sample_lda_result_file = os.path.join(CURRENT_DIR_PATH, "lda_testing_result_May5.csv")
	# sample_w2v_result_file = os.path.join(CURRENT_DIR_PATH, "w2v_google_news_300d_para_wmd_Mar16.csv")
	# it = integration_test()
	# it.load_all_three_result(sample_ec_result_file, sample_lda_result_file, sample_w2v_result_file)
	# it.standarid_result()

	# # it.integrate(0.5, 0.5, 0)
	# # for i in xrange(0, 101, 5):
	# # 	it.evaluate_percentile(i)
	# for i in xrange(101):
	# 	j = 0
	# 	while i + j <= 100:
	# 		weight1 = i / 100.0
	# 		weight2 = j / 100.0
	# 		weight3 = (100 - i - j) / 100.0
	# 		it.integrate(weight1, weight2, weight3)
	# 		it.evaluate_percentile_best_return(weight1, weight2, weight3)
	# 		j += 1

	p = Pool(3)
	print(p.map(try_pool, xrange(101)))