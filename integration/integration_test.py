# -*- coding: utf-8 -*-
import csv
import sys
import os

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



class integration_test:
	def __init__(self):
		def __init__(self):
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		self._load_testing_data()
		self.ec_result = []
		self.lda_result = []
		self.w2v_result = []


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


	def load_all_three_result(self, ec_res, lda_res, w2v_res):
		self.load_ec_result(ec_res)
		self.load_lda_result(lda_res)
		self.load_w2v_result(w2v_res)


	def load_ec_result(self, ec_result_file_path):
		raw_result = read_listOfList_from_CSV(ec_result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)/2):
				result_for_a_sentence.append((row[2*i].lower(), row[2*i+1]))
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=True)
			result_list.append(sorted_result)
		self.ec_result = result_list


	def load_lda_result(self, lda_result_file_path):
		raw_result = read_listOfList_from_CSV(ec_result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)/2):
				result_for_a_sentence.append((row[2*i].lower(), row[2*i+1]))
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=True)
			result_list.append(sorted_result)
		self.lda_result = result_list


	"""
		note: the result form w2v is not nessarily the larger the value, the better
	"""
	def load_w2v_result(self, w2v_result_file_path, reverse_option=True):
		raw_result = read_listOfList_from_CSV(w2v_result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)/2):
				result_for_a_sentence.append((row[2*i].lower(), row[2*i+1]))
			sorted_result = sorted(result_for_a_sentence, key=itemgetter(1), reverse=reverse_option)
			result_list.append(sorted_result)
		self.w2v_result = result_list


	def standarid_result(self):
		pass


	def integrate(self, ec_weight, lda_weight, w2v_weight):
		pass


	"""
		Get the testing result.
		  Percentile will be used to determine which results will be accepted
		  percentile goes from 1 ~ 100
	"""
	def evaluate_percentile(self, percentile):
		if len(self.ground_truth) != len(self.ec_result):
			print "[Warning] Lenth of EC result and the ground truth do not match"
			print "testing/ground truth:", len(self.ec_result), len(self.ground_truth)
		if len(self.ground_truth) != len(self.lda_result):
			print "[Warning] Lenth of LDA result and the ground truth do not match"
			print "testing/ground truth:", len(self.lda_result), len(self.ground_truth)
		if len(self.ground_truth) != len(self.w2v_result):
			print "[Warning] Lenth of W2V result and the ground truth do not match"
			print "testing/ground truth:", len(self.w2v_result), len(self.ground_truth)
		percentile = int(percentile)
		if percentile < 0 or percentile > 100:
			print "[Error] percentile should be a non-negative integer lower than 101"
			return
		tp, p_hat, p = 0, 0, 0
		rank_list = []
		for i in xrange(min(len(self.ground_truth), len(self.result))):
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





def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList


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


if __name__ == "__main__":
	sample_ec_result_file = os.path.join(CURRENT_DIR_PATH, "ec_test_result.csv")
	sample_lda_result_file = os.path.join(CURRENT_DIR_PATH, "lda_testing_result_May5.csv")
	sample_w2v_result_file = os.path.join(CURRENT_DIR_PATH, "w2v_google_news_300d_para_wmd_Mar16.csv")

