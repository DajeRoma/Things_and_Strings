from util import write_listOfList_to_CSV

import wikipedia
from bs4 import BeautifulSoup
import urllib2
import os


current_dir_path = os.path.dirname(os.path.realpath(__file__))


URL_MOST_COMMON_US_PLACE_NAME = "https://en.wikipedia.org/wiki/List_of_the_most_common_U.S._place_names"


def grab_wiki_most_common_us_place_name(url=URL_MOST_COMMON_US_PLACE_NAME):
	webPageHTML = urllib2.urlopen(url).read()
	soup = BeautifulSoup(webPageHTML, "html.parser")
	tables = soup.find_all("table", attrs={"class": "wikitable"})
	assert len(tables)==32  # should be 32
	tableContent = []
	for table in tables:
		trs = table.find_all("tr")
		for row in trs[1:]:
			tds = row.find_all("td")
			assert len(tds)==2
			if "/wiki/" in tds[0].find("a")["href"]:
				record = [tds[0].get_text(), "https://en.wikipedia.org"+tds[0].find("a")["href"], tds[1].get_text()]
			# record = [td.get_text() for td in row.find_all("td")]
			tableContent.append(record)
	# for i in tableContent:
	# 	print i
	return tableContent



class wiki:
	def __init__(self):
		pass


	"""
	Search by a keyword; return by a list of wiki entities
	  sample: [u'Washington', u'Washington (state)', u'Denzel Washington', u'Washington Monument', u'George Washington', u'The Washington Post', u'University of Washington', u'Washington Nationals', u'Washington, Pennsylvania', u'List of Governors of Washington']
	"""
	@staticmethod
	def search(keyword):
		return wikipedia.search(keyword)


	"""
	Given a keyword, if it has a disambiguation page, return a list of entities
	  otherwise, return the page of the entity of the keyword
	"""
	@staticmethod
	def get_disambiguation_list(keyword):
		try:
			wikipage = wikipedia.page(keyword)
			print "No disambiguation"
			return wikipage
		except Exception as e:
			exceptInfo = str(e)
			# print exceptInfo
			entityList = exceptInfo.split('\n')
			return entityList[1:-2]


	@staticmethod
	def get_wiki_content(entity):
		try:
			return wikipedia.page(entity).content.encode('utf-8')
		except Exception as e:
			print '"'+entity+'" is ambiguous'
			print str(e)


	@staticmethod
	def clean_wiki_content(wikiContent):
		pass




if __name__ == '__main__':
	# print wiki.search("washington")
	# for entry in wiki.get_disambiguation_list("washington"):
	# 	wiki.get_wiki_content(entry)
	# print wiki.get_wiki_content("new york")


	placeNameList = grab_wiki_most_common_us_place_name()
	write_listOfList_to_CSV(placeNameList, os.path.join(current_dir_path, "grab_wiki_most_common_us_place_name.csv"))