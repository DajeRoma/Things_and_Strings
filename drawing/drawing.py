import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
from matplotlib.cbook import get_sample_data
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
import matplotlib.image as image

import os, csv

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def draw_F1_to_percentile_logo():
	# fname = get_sample_data('percent_bachelors_degrees_women_usa.csv')
	# gender_degree_data = csv2rec(fname)
	# print type(gender_degree_data)
	# print len(gender_degree_data.year), gender_degree_data.year
	# print len(gender_degree_data["health_professions"]), gender_degree_data["health_professions"]

	# These are the colors that will be used in the plot
	color_sequence = ['#FF0000', '#0000FF', '#00FF00', '#FFA500']
	# color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
	# 				  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
	# 				  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
	# 				  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

	# You typically want your plot to be ~1.33x wider than tall. This plot
	# is a rare exception because of the number of lines being plotted on it.
	# Common sizes: (10, 7.5) and (12, 9)
	fig, ax = plt.subplots(1, 1, figsize=(15, 9))

	# Remove the plot frame lines. They are unnecessary here.
	ax.spines['top'].set_visible(False)	
	ax.spines['right'].set_visible(False)
	# ax.spines['bottom'].set_visible(False)
	# ax.spines['left'].set_visible(False)

	# Ensure that the axis ticks only show up on the bottom and left of the plot.
	# Ticks on the right and top of the plot are generally unnecessary.
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	fig.subplots_adjust(left=.06, right=.84, bottom=.08, top=.94)
	# Limit the range of the plot to only where the data is.
	# Avoid unnecessary whitespace.
	# ax.set_xlim(0, 1)
	ax.set_ylim(0, 0.28)

	# Make sure your axis ticks are large enough to be easily read.
	# You don't want your viewers squinting to read your plot.
	plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], fontsize=14)
	plt.yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25], fontsize=14)
	# ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
	# ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))

	# Provide tick lines across the plot to help your viewers trace along
	# the axis ticks. Make sure that the lines are light and small so they
	# don't obscure the primary data lines.
	plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

	# Remove the tick marks; they are unnecessary with the tick lines we just
	# plotted.
	plt.tick_params(axis='both', which='both', bottom='off', top='off',
					labelbottom='on', left='off', right='off', labelleft='on')

	# Now that the plot is prepared, it's time to actually plot the data!
	# Note that I plotted the majors in order of the highest % in the final year.
	majors = ['Health Professions', 'Public Administration', 'Education',
			  'Psychology', 'Foreign Languages', 'English',
			  'Communications\nand Journalism', 'Art and Performance', 'Biology',
			  'Agriculture', 'Social Sciences and History', 'Business',
			  'Math and Statistics', 'Architecture', 'Physical Sciences',
			  'Computer Science', 'Engineering']

	y_offsets = {'Foreign Languages': 0.5, 'English': -0.5,
				 'Communications\nand Journalism': 0.75,
				 'Art and Performance': -0.25, 'Agriculture': 1.25,
				 'Social Sciences and History': 0.25, 'Business': -0.75,
				 'Math and Statistics': 0.75, 'Architecture': -0.75,
				 'Computer Science': 0.75, 'Engineering': -0.25}

	y_axis_offset = 0.0026
	line = plt.plot((0, 1), (0.0687816582, 0.0687816582), 'k-',
						lw=2.5,
						color=color_sequence[0])
	# plt.text(1.01, 0.0687816582-y_axis_offset, "DBpedia Spotlight", fontsize=22, color=color_sequence[0])
	line = plt.plot((0, 1), (0.1220999287, 0.1220999287), 'k-',
						lw=2.5,
						color=color_sequence[1])
	# plt.text(1.01, 0.1220999287-y_axis_offset, "Open Calais", fontsize=22, color=color_sequence[1])
	line = plt.plot((0, 1), (0.0930958714, 0.0930958714), 'k-',
						lw=2.5,
						color=color_sequence[2])
	# plt.text(1.01, 0.0930958714-y_axis_offset, "TextRazor", fontsize=22, color=color_sequence[2])

	ts_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "31-22-47.csv"))
	percentile_f1 = {}
	percentile = []
	f1 = []
	for row in ts_data:
		percentile_f1[float(row[3][:row[3].find("th")])/100] = float(row[7])
	for key in sorted(percentile_f1.keys()):
		percentile.append(key)
		f1.append(percentile_f1[key])
	line = plt.plot(percentile,
					f1,
					lw=2.5,
					color=color_sequence[3])

	dbsl_logo = get_sample_data(os.path.join(CURRENT_DIR_PATH, "logo_dbsl.png"))
	tr_logo = get_sample_data(os.path.join(CURRENT_DIR_PATH, "logo_textrazor.png"))
	oc_logo = get_sample_data(os.path.join(CURRENT_DIR_PATH, "logo_opencalais.png"))
	ts_logo = get_sample_data(os.path.join(CURRENT_DIR_PATH, "stko_logo.png"))
	dbsl_logo = plt.imread(dbsl_logo)
	tr_logo = plt.imread(tr_logo)
	oc_logo = plt.imread(oc_logo)
	ts_logo = plt.imread(ts_logo)
	newax1 = fig.add_axes([0.855, 0.23, 0.08, 0.08], anchor='NE', zorder=1)
	newax1.imshow(dbsl_logo)
	newax1.axis('off')
	newax2 = fig.add_axes([0.86, 0.27, 0.12, 0.12], anchor='NE', zorder=1)
	newax2.imshow(tr_logo)
	newax2.axis('off')
	newax3 = fig.add_axes([0.858, 0.42, 0.1, 0.1], anchor='NE', zorder=1)
	newax3.imshow(oc_logo)
	newax3.axis('off')
	newax4 = fig.add_axes([0.82, 0.745, 0.1, 0.1], anchor='NE', zorder=1)
	newax4.imshow(ts_logo)
	newax4.axis('off')

	# for rank, column in enumerate(majors):
	# 	# Plot each line separately with its own color.
	# 	column_rec_name = column.replace('\n', '_').replace(' ', '_').lower()

	# 	line = plt.plot(gender_degree_data.year,
	# 					gender_degree_data[column_rec_name],
	# 					lw=2.5,
	# 					color=color_sequence[rank])

	# 	# Add a text label to the right end of every line. Most of the code below
	# 	# is adding specific offsets y position because some labels overlapped.
	# 	y_pos = gender_degree_data[column_rec_name][-1] - 0.5

	# 	if column in y_offsets:
	# 		y_pos += y_offsets[column]

	# 	# Again, make sure that all labels are large enough to be easily read
	# 	# by the viewer.
	# 	plt.text(2011.5, y_pos, column, fontsize=14, color=color_sequence[rank])

	# Make the title big enough so it spans the entire plot, but don't make it
	# so big that it requires two lines to show.

	# Note that if the title is descriptive enough, it is unnecessary to include
	# axis labels; they are self-evident, in this plot's case.
	# fig.suptitle('Percentage of Bachelor\'s degrees conferred to women in '
	#              'the U.S.A. by major (1970-2011)\n', fontsize=18, ha='center')

	# Finally, save the figure as a PNG.
	# You can also save it as a PDF, JPEG, etc.
	# Just change the file extension in this call.
	# plt.savefig('percent-bachelors-degrees-women-usa.png', bbox_inches='tight')
	# plt.show()
	plt.savefig('figure.png', dpi = 100)


def draw_F1_to_percentile():
	# These are the colors that will be used in the plot
	color_sequence = ['cyan', '#0000FF', 'magenta']

	fig, ax = plt.subplots(1, 1, figsize=(15, 9))

	ax.spines['top'].set_visible(False)	
	ax.spines['right'].set_visible(False)

	# Ensure that the axis ticks only show up on the bottom and left of the plot.
	# Ticks on the right and top of the plot are generally unnecessary.
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	fig.subplots_adjust(left=.08, right=.9, bottom=.15, top=.98)
	# Limit the range of the plot to only where the data is.
	# Avoid unnecessary whitespace.
	# ax.set_xlim(0, 1)
	ax.set_ylim(0, 0.28)

	# Make sure your axis ticks are large enough to be easily read.
	# You don't want your viewers squinting to read your plot.
	plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], fontsize=14)
	plt.yticks([0.05, 0.1, 0.15, 0.2, 0.25], fontsize=14)
	# ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
	# ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))

	# Provide tick lines across the plot to help your viewers trace along
	# the axis ticks. Make sure that the lines are light and small so they
	# don't obscure the primary data lines.
	plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

	# Remove the tick marks; they are unnecessary with the tick lines we just
	# plotted.
	plt.tick_params(axis='both', which='both', bottom='off', top='off',
					labelbottom='on', left='off', right='off', labelleft='on')

	# y_axis_offset = 0.0026
	line = plt.plot((0, 100), (0.0687816582, 0.0687816582), 'k-',
						lw=4,
						color="navy",
						label="DBpedia Spotlight")
	# plt.text(1.01, 0.0687816582-y_axis_offset, "DBpedia Spotlight", fontsize=22, color=color_sequence[0])
	line = plt.plot((0, 100), (0.1220999287, 0.1220999287), 'k-',
						lw=4,
						color="deepskyblue",
						label="Open Calais")
	# plt.text(1.01, 0.1220999287-y_axis_offset, "Open Calais", fontsize=22, color=color_sequence[1])
	line = plt.plot((0, 100), (0.0930958714, 0.0930958714), 'k-',
						lw=4,
						color="blue",
						label="TextRazor")
	# plt.text(1.01, 0.0930958714-y_axis_offset, "TextRazor", fontsize=22, color=color_sequence[2])

	ts_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "31-22-47.csv"))
	percentile_f1 = {}
	percentile = []
	f1 = []
	for row in ts_data:
		percentile_f1[float(row[3][:row[3].find("th")])] = float(row[7])
	for key in sorted(percentile_f1.keys()):
		percentile.append(key)
		f1.append(percentile_f1[key])
	line = plt.plot(percentile,
					f1,
					lw=4,
					color="r",
					label="TSM")
	ax.legend(loc='upper left', fontsize=20)
	ax.set_xlabel('Percentile', fontsize=20)
	ax.set_ylabel('F-score', fontsize=20)
	plt.savefig('figure.png', dpi = 100)


def draw_precisionAt1_to_percentile():
	# These are the colors that will be used in the plot
	color_sequence = ['cyan', '#0000FF', 'magenta']

	fig, ax = plt.subplots(1, 1, figsize=(15, 9))

	ax.spines['top'].set_visible(False)	
	ax.spines['right'].set_visible(False)

	# Ensure that the axis ticks only show up on the bottom and left of the plot.
	# Ticks on the right and top of the plot are generally unnecessary.
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	fig.subplots_adjust(left=.08, right=.9, bottom=.15, top=.98)
	# Limit the range of the plot to only where the data is.
	# Avoid unnecessary whitespace.
	# ax.set_xlim(0, 1)
	ax.set_ylim(0, 0.28)

	# Make sure your axis ticks are large enough to be easily read.
	# You don't want your viewers squinting to read your plot.
	plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], fontsize=14)
	plt.yticks([0.05, 0.1, 0.15, 0.2, 0.25], fontsize=14)
	# ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
	# ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))

	# Provide tick lines across the plot to help your viewers trace along
	# the axis ticks. Make sure that the lines are light and small so they
	# don't obscure the primary data lines.
	plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

	# Remove the tick marks; they are unnecessary with the tick lines we just
	# plotted.
	plt.tick_params(axis='both', which='both', bottom='off', top='off',
					labelbottom='on', left='off', right='off', labelleft='on')

	# y_axis_offset = 0.0026
	line = plt.plot((0, 100), (0.062015503876, 0.062015503876), 'k-',
						lw=4,
						color="navy",
						label="DBpedia Spotlight")
	# plt.text(1.01, 0.0687816582-y_axis_offset, "DBpedia Spotlight", fontsize=22, color=color_sequence[0])
	line = plt.plot((0, 100), (0.156471781007, 0.156471781007), 'k-',
						lw=4,
						color="deepskyblue",
						label="Open Calais")
	# plt.text(1.01, 0.1220999287-y_axis_offset, "Open Calais", fontsize=22, color=color_sequence[1])
	line = plt.plot((0, 100), (0.0309148264984, 0.0309148264984), 'k-',
						lw=4,
						color="blue",
						label="TextRazor")
	# plt.text(1.01, 0.0930958714-y_axis_offset, "TextRazor", fontsize=22, color=color_sequence[2])

	ts_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "31-22-47.csv"))
	percentile_f1 = {}
	percentile = []
	f1 = []
	for row in ts_data:
		percentile_f1[float(row[3][:row[3].find("th")])] = float(row[7])
	for key in sorted(percentile_f1.keys()):
		percentile.append(key)
		f1.append(percentile_f1[key])
	line = plt.plot(percentile,
					f1,
					lw=4,
					color="r",
					label="TSM")
	ax.legend(loc='upper left', fontsize=20)
	ax.set_xlabel('Percentile', fontsize=20)
	ax.set_ylabel('F-score', fontsize=20)
	plt.savefig('figure.png', dpi = 100)



def draw_F1_to_percentile_noTSM():
	# These are the colors that will be used in the plot
	color_sequence = ['cyan', '#0000FF', 'magenta']

	fig, ax = plt.subplots(1, 1, figsize=(15, 9))

	ax.spines['top'].set_visible(False)	
	ax.spines['right'].set_visible(False)

	# Ensure that the axis ticks only show up on the bottom and left of the plot.
	# Ticks on the right and top of the plot are generally unnecessary.
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	fig.subplots_adjust(left=.08, right=.95, bottom=.15, top=.95)
	# Limit the range of the plot to only where the data is.
	# Avoid unnecessary whitespace.
	# ax.set_xlim(0, 1)
	ax.set_ylim(0, 0.23)

	# Make sure your axis ticks are large enough to be easily read.
	# You don't want your viewers squinting to read your plot.
	plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], fontsize=14)
	plt.yticks([0.05, 0.1, 0.15, 0.2], fontsize=14)
	# ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
	# ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))

	# Provide tick lines across the plot to help your viewers trace along
	# the axis ticks. Make sure that the lines are light and small so they
	# don't obscure the primary data lines.
	plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

	# Remove the tick marks; they are unnecessary with the tick lines we just
	# plotted.
	plt.tick_params(axis='both', which='both', bottom='off', top='off',
					labelbottom='on', left='off', right='off', labelleft='on')

	# y_axis_offset = 0.0026
	line = plt.plot((0, 100), (0.0687816582, 0.0687816582), 'k-',
						lw=4,
						color="navy",
						label="DBpedia Spotlight")
	# plt.text(1.01, 0.0687816582-y_axis_offset, "DBpedia Spotlight", fontsize=22, color=color_sequence[0])
	line = plt.plot((0, 100), (0.1220999287, 0.1220999287), 'k-',
						lw=4,
						color="deepskyblue",
						label="Open Calais")
	# plt.text(1.01, 0.1220999287-y_axis_offset, "Open Calais", fontsize=22, color=color_sequence[1])
	line = plt.plot((0, 100), (0.0930958714, 0.0930958714), 'k-',
						lw=4,
						color="blue",
						label="TextRazor")
	# plt.text(1.01, 0.0930958714-y_axis_offset, "TextRazor", fontsize=22, color=color_sequence[2])

	pr_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "entitycooccurrence.csv"))
	percentile_f1 = {}
	percentile = []
	f1 = []
	for row in pr_data:
		percentile_f1[float(row[3][:row[3].find("th")])] = float(row[7])
	for key in sorted(percentile_f1.keys()):
		percentile.append(key)
		f1.append(percentile_f1[key])
	line = plt.plot(percentile,
					f1,
					lw=4,
					color="y",
					label="Entity Co-occurrence")
	pr_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "topicmodel.csv"))
	percentile_f1 = {}
	percentile = []
	f1 = []
	for row in pr_data:
		percentile_f1[float(row[3][:row[3].find("th")])] = float(row[7])
	for key in sorted(percentile_f1.keys()):
		percentile.append(key)
		f1.append(percentile_f1[key])
	line = plt.plot(percentile,
					f1,
					lw=4,
					color="orange",
					label="Topic Model")
	pr_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "wordembedding.csv"))
	percentile_f1 = {}
	percentile = []
	f1 = []
	for row in pr_data:
		percentile_f1[float(row[3][:row[3].find("th")])] = float(row[7])
	for key in sorted(percentile_f1.keys()):
		percentile.append(key)
		f1.append(percentile_f1[key])
	line = plt.plot(percentile,
					f1,
					lw=4,
					color="Salmon",
					label="Word Embedding")
	ax.legend(loc='upper left', fontsize=20)
	ax.set_xlabel('Percentile', fontsize=20)
	ax.set_ylabel('F-score', fontsize=20)
	plt.savefig('figure.png', dpi = 100)


def plot_precion_recall_curve():
	plt.clf()
	fig, ax = plt.subplots(1, 1, figsize=(15, 9))
	fig.subplots_adjust(left=.07, right=.95)	
	ax.set_xlim(0, 1.05)
	ax.set_ylim(0, 0.26)
	plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], fontsize=15)
	plt.yticks([0.05, 0.1, 0.15, 0.2, 0.25], fontsize=15)

	pr_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "31-22-47.csv"))
	precision_recall = {}
	recall = []
	for row in pr_data:		
		recall.append(float(row[10]))
		precision_recall[float(row[10])] = float(row[9])
	recall = sorted(recall)
	precision = []
	for rec in recall:
		precision.append(precision_recall[rec])
	line = plt.plot(recall,
					precision,
					lw=4,
					color="r",
					label="Things & Strings Model")

	pr_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "topicmodel.csv"))
	precision_recall = {}
	recall = []
	for row in pr_data:		
		recall.append(float(row[10]))
		precision_recall[float(row[10])] = float(row[9])
	recall = sorted(recall)
	precision = []
	for rec in recall:
		precision.append(precision_recall[rec])
	line = plt.plot(recall,
					precision,
					lw=4,
					color="orange",
					label="Topic Model")
	pr_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "wordembedding.csv"))
	precision_recall = {}
	recall = []
	for row in pr_data:		
		recall.append(float(row[10]))
		precision_recall[float(row[10])] = float(row[9])
	recall = sorted(recall)
	precision = []
	for rec in recall:
		precision.append(precision_recall[rec])
	line = plt.plot(recall,
					precision,
					lw=4,
					color="Salmon",
					label="Word Embedding")

	pr_data = read_listOfList_from_CSV(os.path.join(CURRENT_DIR_PATH, "entitycooccurrence.csv"))
	precision_recall = {}
	recall = []
	for row in pr_data:		
		recall.append(float(row[10]))
		precision_recall[float(row[10])] = float(row[9])
	recall = sorted(recall)
	precision = []
	for rec in recall:
		precision.append(precision_recall[rec])
	line = plt.plot(recall,
					precision,
					lw=4,
					color="y",
					label="Entity Co-occurrence")


	ax.set_xlabel('Recall', fontsize=20)
	ax.set_ylabel('Precision', fontsize=20)
	ax.legend(loc='upper right', fontsize=20)
	# plt.show()
	plt.savefig('precision_recall_curve.png', dpi = 100)


def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList




if __name__ == '__main__':
	draw_F1_to_percentile()

	# plot_precion_recall_curve()

	# draw_F1_to_percentile_noTSM()