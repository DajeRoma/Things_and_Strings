'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import os, csv

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList


data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "comprehensive_summary_June27.csv"))
data_dict = {}
print len(data)/101
counter = 0
for row in data:	
	w1, w2, w3 = str(int(round(float(row[0])*100))), str(int(round(float(row[1])*100))), str(int(round(float(row[2])*100)))
	if int(w1) + int(w2) + int(w3) != 100:
		print row[0], row[1], row[2]
		print w1, w2, w3
	f1 = float(row[7])
	if len(w1) == 1:
		w1 = '00' + w1
	if len(w1) == 2:
		w1 = '0' + w1
	if len(w2) == 1:
		w2 = '00' + w2
	if len(w2) == 2:
		w2 = '0' + w2
	if len(w3) == 1:
		w3 = '00' + w3
	if len(w3) == 2:
		w3 = '0' + w3
	temp_key = w1 + '_' +  w2 + '_' +  w3
	if temp_key not in data_dict:
		data_dict[temp_key] = f1
		# print counter, temp_key
		counter = 1
	else:
		if f1 > data_dict[temp_key]:
			data_dict[temp_key] = f1
		counter += 1
X, Y, Z = [], [], []
V = []
for key in sorted(data_dict.keys()):
	X.append(int(key[:3]))
	Y.append(int(key[4:7]))
	Z.append(int(key[8:]))
	V.append(data_dict[key])
print len(data_dict.keys())


fig = plt.figure(figsize=(80, 60))
ax = fig.add_subplot(111, projection='3d')

sp = ax.scatter(X, Y, Z, s=20, c=V)
plt.colorbar(sp)
ax.set_xlabel('Entity Co-occurrence Weight')
ax.set_ylabel('Topic Model Weight')
ax.set_zlabel('Word Embedding Weight')
ax.view_init(elev=30, azim=35)
plt.show()

