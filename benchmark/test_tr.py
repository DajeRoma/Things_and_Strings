# -*- coding: utf-8 -*-
import csv
import json
import os

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

TESTING_SENTENCES_FILE_PATH = os.path.join(
		os.path.dirname(CURRENT_DIR_PATH),
		"testing_data",
		"testing_sentence_city_ambiPlaceName_Mar14.csv")

US_STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",  "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


class test_tr():
	def __init__(self):
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		self.load_testing_data()
		self.result = []


	def load_testing_data(self, testingDataFilePath=TESTING_SENTENCES_FILE_PATH):
		listOfList = read_listOfList_from_CSV(testingDataFilePath)
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		for row in listOfList:
			self.testing_sentences.append(row[0])
			self.ground_truth.append(row[1])
			self.annoted_place_names.append(row[2])	


	def load_result_data(self, result_file_path):
		raw_result = read_listOfList_from_CSV(result_file_path)
		result_list= []
		for row in raw_result:
			result_for_a_sentence = []
			for i in xrange(len(row)):
				result_for_a_sentence.append(row[i].lower())
			result_list.append(result_for_a_sentence)
		self.result = result_list


	def evaluate(self):
		if len(self.ground_truth) != len(self.result):
			print "[Warning] Lenth of the ground truth and the result do not match"
			print "testing/ground truth:", len(self.result), len(self.ground_truth) 
		tp, p_hat, p = 0, 0, 0
		rank_list = []
		for i in xrange(min(len(self.ground_truth), len(self.result))):
			p += 1
			result_for_a_sentence = self.result[i]
			for j in xrange(len(result_for_a_sentence)):
				p_hat += 1
				# if str(result_for_a_sentence[j]).lower() == str(self.ground_truth[i]).lower():
				if compare(str(result_for_a_sentence[j]).lower(), str(self.ground_truth[i]).lower()):	
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


def compare(place_name1, place_name2):
	for state_name in US_STATES:
		state_name = state_name.lower()
		if state_name in place_name1 and state_name in place_name2:
			return True
	return False



def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList


if __name__ == "__main__":
	test_case = test_tr()

	test_case.load_result_data(os.path.join(CURRENT_DIR_PATH, 
									"textrazor",
									"textrazor_result.csv"))
	test_case.evaluate()