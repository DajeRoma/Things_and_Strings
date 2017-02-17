import csv


def write_listOfList_to_CSV(listOfList, csv_file_path):
	with open(csv_file_path, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for listEntry in listOfList:
			spamwriter.writerow(listEntry)