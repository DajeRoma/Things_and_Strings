import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
from matplotlib.cbook import get_sample_data
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
import matplotlib.image as image

import os, csv

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def draw_F1_to_percentile():
	fname = get_sample_data('percent_bachelors_degrees_women_usa.csv')
	gender_degree_data = csv2rec(fname)
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

	fig.subplots_adjust(left=.06, right=.75, bottom=.02, top=.94)
	# Limit the range of the plot to only where the data is.
	# Avoid unnecessary whitespace.
	# ax.set_xlim(0, 1)
	ax.set_ylim(0, 0.28)

	# Make sure your axis ticks are large enough to be easily read.
	# You don't want your viewers squinting to read your plot.
	plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], fontsize=14)
	plt.yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3], fontsize=14)
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
	newax1 = fig.add_axes([0.755, 0.18, 0.08, 0.08], anchor='NE', zorder=1)
	newax1.imshow(dbsl_logo)
	newax1.axis('off')
	newax2 = fig.add_axes([0.76, 0.208, 0.12, 0.12], anchor='NE', zorder=1)
	newax2.imshow(tr_logo)
	newax2.axis('off')
	newax3 = fig.add_axes([0.758, 0.35, 0.08, 0.08], anchor='NE', zorder=1)
	newax3.imshow(oc_logo)
	newax3.axis('off')
	newax4 = fig.add_axes([0.72, 0.67, 0.1, 0.1], anchor='NE', zorder=1)
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
	plt.show()


def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList




if __name__ == '__main__':
	draw_F1_to_percentile()