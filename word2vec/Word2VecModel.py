# -*- coding: utf-8 -*-

import os, codecs
import fileinput
from gensim.models.word2vec import Word2Vec
from nltk.corpus import stopwords
import nltk.data
import sys, inspect
import numpy as np
from numpy import dot
from gensim import matutils
from nltk.tokenize import WordPunctTokenizer, word_tokenize

# from util import tokenized_to_words


reload(sys)  
sys.setdefaultencoding('utf8')

W2V_TRAINED_MODEL_FOLDER_PATH = '/home/yiting/data_ThingsString'



class Word2VecModel:
	def __init__(self):
		self.model = None
		self._vocabDict = {}



	def _update_model_dict(self):
		self._vocabDict = self.model.vocab


	def get_model_dict(self):
		return self._vocabDict


	def get_model_keys(self):
		return self._vocabDict.keys()


	def get_word_vector(self, word):
		if word in self._vocabDict.keys():
			return self.model[word]
		else:
			return None


	def get_average_words_vectors(self, wordList):
		sum_vectors = []
		counter = 0
		for word in wordList:
			wordVec = self.get_word_vector(word)
			if wordVec is not None:
				if len(sum_vectors) == 0:
					sum_vectors = wordVec
					counter +=1
				else:
					sum_vectors = np.sum([sum_vectors, wordVec], axis=0)
					counter +=1
		return np.divide(sum_vectors, float(counter))


	def get_wordwise_similarity(self, word1, word2):
		return self.model.similarity(word1, word2)


	"""
		Load a trained word2vec model 
		  from a .txt file [binary=False] or a C file [binary=True]
		**Note that for .txt file, the first line should be 
			<# of lines> <# of dimensions>
	"""
	def load_w2v_model(self, modelFilePath, binary=False):
		model = Word2Vec.load_word2vec_format(modelFilePath, binary=binary)
		self.model = model
		self._update_model_dict()
		print "[info] Model is loaded"


	"""
		Get dissimilarity between two sentences using Word Mover's Distance
	"""
	def get_sents_dif_wmd(self, sent1, sent2, stopword=True):
		sent1List = []
		sent2List = []
		if stopword:
			stopwordList = stopwords.words('english')
			sent1List = [word.lower() for word \
							in tokenized_to_words(sent1) \
								if word not in stopwordList \
								and word in self._vocabDict]
			sent2List = [word.lower() for word \
							in tokenized_to_words(sent2) \
								if word not in stopwordList \
								and word in self._vocabDict]
		else:
			sent1List = [word.lower() for word \
							in tokenized_to_words(sent1) \
								if word in self._vocabDict]
			sent2List = [word.lower() for word \
							in tokenized_to_words(sent2) \
								if word in self._vocabDict]
		# Note that if one of the documents have no words that exist in the
		#   Word2Vec vocab, `float('inf')` (i.e. infinity) will be returned.
		return self.model.wmdistance(sent1List, sent2List)		
		# if stopword:
		# 	stopwordList = stopwords.words('english')
		# 	sent1List = [word.lower() for word in sent1.split() if word not in stopwordList]
		# 	sent2List = [word.lower() for word in sent2.split() if word not in stopwordList]
		# else:
		# 	sent1List = [word.lower() for word in sent1.split() if word in self._vocabDict]
		# 	sent2List = [word.lower() for word in sent2.split() if word in self._vocabDict]
		# # Note that if one of the documents have no words that exist in the
		# #   Word2Vec vocab, `float('inf')` (i.e. infinity) will be returned.
		# return self.model.wmdistance(sent1List, sent2List)


	"""
		Get similarity between two sentences using average vectors and 
		  cosine similarity
	"""
	def get_sents_similarity_avgvec(self, sent1, sent2, stopword=True):
		sent1List = []
		sent2List = []
		if stopword:
			stopwordList = stopwords.words('english')
			sent1List = [word.lower() for word \
							in tokenized_to_words(sent1) \
								if word not in stopwordList \
								and word in self._vocabDict]
			sent2List = [word.lower() for word \
							in tokenized_to_words(sent2) \
								if word not in stopwordList \
								and word in self._vocabDict]
		else:
			sent1List = [word.lower() for word \
							in tokenized_to_words(sent1) \
								if word in self._vocabDict]
			sent2List = [word.lower() for word \
							in tokenized_to_words(sent2) \
								if word in self._vocabDict]
		sent1Vec = self.get_average_words_vectors(sent1List)
		sent2Vec = self.get_average_words_vectors(sent2List)
		return dot(matutils.unitvec(sent1Vec), matutils.unitvec(sent2Vec))


	"""
		Get dissimilarity between two paragraphs using Word Mover's Distance
		  note: 1. paragraphs will be split into sentences. 
		  		2. each paragraph will generate a score
		  		3. the lowest score will be picked
	"""
	def get_paragraphs_dif_wmd(self, training_para, testing_sent, stopword=True):
		training_para_list = []
		testing_sent_list = []
		if stopword:
			stopwordList = stopwords.words('english')
			for temp_sent in tokenize_to_sents(training_para):
				temp_list = [word.lower() for word \
							in tokenize_sent_to_words(temp_sent) \
								if word not in stopwordList \
								and word in self._vocabDict]
				training_para_list.append(temp_list)
			testing_sent_list = [word.lower() for word \
							in tokenized_to_words(testing_sent) \
								if word not in stopwordList \
								and word in self._vocabDict]
		else:
			for temp_sent in tokenize_to_sents(training_para):
				temp_list = [word.lower() for word \
							in tokenize_sent_to_words(temp_sent) \
								if word in self._vocabDict]
				training_para_list.append(temp_list)
			testing_sent_list = [word.lower() for word \
							in tokenized_to_words(testing_sent) \
								if word in self._vocabDict]
		# Note that if one of the documents have no words that exist in the
		#   Word2Vec vocab, `float('inf')` (i.e. infinity) will be returned.
		lowest_wmd = 8 	# in general, wmd is lower than 8
		for i in xrange(len(training_para_list)):
			training_sent_list = training_para_list[i]
			if training_sent_list:
				wmd_score = self.model.wmdistance(training_sent_list, testing_sent_list)
				if wmd_score < lowest_wmd:
					lowest_wmd = wmd_score
		return lowest_wmd


	@staticmethod
	def fixTxtModelFile(modelFilePath):
		rowCounter = 0
		colCounter = 0
		f = open(modelFilePath)
		for line in f:
			if rowCounter==0:
				itemList = line.split(' ')
				colCounter = len(itemList)
			rowCounter+=1
		# num_lines = sum(1 for line in open(modelFilePath))
		# print str(rowCounter)+' '+str(colCounter-1)
		Word2VecModel.line_pre_adder(modelFilePath, 
									str(rowCounter)+' '+str(colCounter-1))


	"""
		Insert a line [lineToWrite] at the begining of the file [filename]
	"""
	@staticmethod
	def line_pre_adder(filename, lineToWrite):
		f = fileinput.input(filename, inplace=1)
		for xline in f:
			if f.isfirstline():
				print lineToWrite.rstrip('\r\n') + '\n' + xline,
			else:
				print xline,


"""
	Given a string, tokenize the string into a list of sentences
		Punkt Sentence Tokenizer
"""
def tokenize_to_sents(text):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sents = [sent.strip() for sent in sent_detector.tokenize(text.strip())]
	return sents


"""
	Given a string, tokenize the string (a sentence) into a list of words
		Punkt Word Tokenizer
"""
def tokenize_sent_to_words(sent):
	return word_tokenize(sent)


"""
	Given a string, tokenize the string (one or multiple sentences) into 
	  a list of sentences first and then to words
		Punkt Sentence Tokenizer + Punkt Word Tokenizer
"""
def tokenized_to_words(text):
	words = []
	text = codecs.utf_8_decode(text.encode('utf8'))
	text = text[0]
	for sent in tokenize_to_sents(text):
		words.extend(tokenize_sent_to_words(sent))
	return words








if __name__ == "__main__":
	trained_model_filePath = os.path.join(W2V_TRAINED_MODEL_FOLDER_PATH, "glove.6B", "glove.6B.200d.txt")
	Word2VecModel.fixTxtModelFile(trained_model_filePath)
	# w2v = Word2VecModel()
	# w2v.load_w2v_model(trained_model_filePath)
	# print w2v.get_wordwise_similarity("princess", "queen")

	# 0.79472449113

	# print w2v.get_word_vector("king")
	# print w2v.model.similarity('king', 'woman')
	# kingVec = w2v.get_word_vector("king")
	# womanVec = w2v.get_word_vector("woman")

	# print dot(matutils.unitvec(kingVec), matutils.unitvec(womanVec))


	# print w2v.get_average_words_vectors(["I", "have", "an", "apple"]), type(w2v.get_average_words_vectors(["I", "have", "an", "apple"]))



	# trained_model_filePath = os.path.join(W2V_TRAINED_MODEL_FOLDER_PATH, "glove.6B", "glove.6B.50d.txt")
	# w2v = Word2VecModel()
	# w2v.load_w2v_model(trained_model_filePath)
	# print w2v.model.similarity('king', 'woman')
	# kingVec = w2v.get_word_vector("king")
	# womanVec = w2v.get_word_vector("woman")

	# print dot(kingVec/np.linalg.norm(kingVec), womanVec/np.linalg.norm(womanVec))
	# print dot(matutils.unitvec(kingVec), matutils.unitvec(womanVec))



	# a = np.asarray([1, 2, 3, 4, 5])
	# print a/np.linalg.norm(a)
	# print matutils.unitvec(a)




	sent1 = """
	Washington, D.C., formally the District of Columbia and commonly referred to as "Washington", "the District", or simply "D.C.", is the capital of the United States.
	"""

	sent2 = """
	Milford is a coastal city in southwestern New Haven County, Connecticut, United States, located between Bridgeport and New Haven.
	"""
	# print w2v.get_sents_dif_wmd(sent1, sent2)
	# print w2v.get_sents_similarity_avgvec(sent1, sent2)
	# print w2v.get_sents_dif_wmd("The president greets the press in Chicago", "Obama speaks to the media in Illinois")
	# print w2v.get_sents_similarity_avgvec("The president greets the press in Chicago", "Obama speaks to the media in Illinois")
	# print w2v.get_sents_dif_wmd("The president greets the press in Chicago", sent2)
	# print w2v.get_sents_similarity_avgvec("The president greets the press in Chicago", sent2)