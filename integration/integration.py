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



class integration_model:
	def __init__(self):
		pass











if __name__ == "__main__":
	pass