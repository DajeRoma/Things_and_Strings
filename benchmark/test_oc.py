# -*- coding: utf-8 -*-
import csv
import requests
import json
import os
from OpenCalais import OpenCalais

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

TESTING_SENTENCES_FILE_PATH = os.path.join(
		os.path.dirname(CURRENT_DIR_PATH),
		"testing_data",
		"testing_sentence_city_ambiPlaceName_Mar14.csv")


class test_oc():
	def __init__(self):
		self.testing_sentences = []
		self.ground_truth = []
		self.annoted_place_names = []
		self.load_testing_data()
		self.result = []


	def run_oc_in_batch(self, output_file_path, start_ind, end_ind):
		if not self.testing_sentences \
			or not self.ground_truth \
			or not self.annoted_place_names:
			print "[Error] No testing data or ground truth"
			return None
		if len(self.testing_sentences) != len(self.ground_truth) \
			or len(self.testing_sentences) != len(self.annoted_place_names):
			print "[Error] No testing data length not match"
			return None
		oc = OpenCalais()
		for i in range(len(self.testing_sentences))[start_ind : end_ind]:
			testing_sent = self.testing_sentences[i].lower()
			surface_form = self.annoted_place_names[i].lower()
			print "[info] Testing sentence No.", str(i+1), "...",
			print "[info]   ambiguous place name: {}"\
						.format(str(surface_form))
			annotation_list = oc.annotate(testing_sent, surface_form)
			# print annotation_list
			write_list_to_row_csv(annotation_list, output_file_path, append=True)



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
				if str(result_for_a_sentence[j]).lower() == str(self.ground_truth[i]).lower():
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



def write_list_to_row_csv(list_to_write, csv_file_path, append=False):
	write_type = "a" if append == True else "wb" 
	with open(csv_file_path, write_type) as csvfile:
		spamwriter = csv.writer(csvfile, delimiter = ',',
								quotechar = '"',
								quoting = csv.QUOTE_MINIMAL)
		spamwriter.writerow([unicode(s).encode("utf-8") for s in list_to_write])



def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList



if __name__ == "__main__":
	test_case = test_oc()
	# test_case.run_oc_in_batch(os.path.join(CURRENT_DIR_PATH, 
	# 								"opencalais",
	# 								"oc_test_result.csv"),
	# 							4900, 5340)
	test_case.load_result_data(os.path.join(CURRENT_DIR_PATH, 
									"opencalais",
									"oc_test_result.csv"))
	test_case.evaluate()