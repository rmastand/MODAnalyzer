from __future__ import division



import hists


from MODPlot import *


import trigger_parse





from subprocess import call

from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedLocator
from matplotlib.ticker import LogLocator
from matplotlib.ticker import FormatStrFormatter

from sets import Set

import time as time
import copy


import sys
import math
from collections import defaultdict

# matplotlib
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerLine2D
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm


# RootPy
from rootpy.plotting import Hist, HistStack, Legend
import rootpy.plotting.root2matplotlib as rplt
from rootpy.plotting import Hist2D


# Stuff for calculating areas.
from scipy.integrate import simps
from scipy import interpolate
from scipy import optimize

from numpy import trapz


from matplotlib import gridspec

import matplotlib.ticker as mtick

from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
from matplotlib.backends.backend_pdf import PdfPages

from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox, AnchoredOffsetbox, HPacker

from mpl_toolkits.axes_grid.anchored_artists import AnchoredDrawingArea

from scipy.stats import norm
from scipy.stats import gamma
from scipy import arange, array, exp

from scipy.stats import binned_statistic

import rootpy.plotting.views




mpl.rcParams['axes.linewidth'] = 5.0 #set the value globally
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
mpl.rcParams['text.latex.preamble'] = [r'\boldmath']

plt.rc('font', family='serif', size=43)




default_dir = "plots/Version 5_2/"


logo_location = "/home/aashish/root/macros/MODAnalyzer/mod_logo.png"
logo_text = "Preliminary"




parsed_linear = trigger_parse.load_root_files_to_hist()


def logo_box():
	
	logo_offset_image = OffsetImage(read_png(get_sample_data(logo_location, asfileobj=False)), zoom=0.25, resample=1, dpi_cor=1)
	text_box = TextArea(logo_text, textprops=dict(color='#444444', fontsize=50, weight='bold'))

	logo_and_text_box = HPacker(children=[logo_offset_image, text_box], align="center", pad=0, sep=25)

	anchored_box = AnchoredOffsetbox(loc=2, child=logo_and_text_box, pad=0.8, frameon=False, borderpad=0., bbox_to_anchor=[0.13, 0.90], bbox_transform = plt.gcf().transFigure)

	return anchored_box



def normalize_hist(hist):
	bin_width = (hist.upperbound() - hist.lowerbound()) / hist.nbins()
	
	if hist.GetSumOfWeights() != 0.0:
		hist.Scale(1.0 / ( hist.GetSumOfWeights() * bin_width ))

	return hist



def trigger_turn_on_curves():

	mod_hists = parsed_linear[0]

	colors = ['green', 'magenta', 'blue', 'red', 'brown', 'orange']
	labels = ["Jet140U", "Jet100U", "Jet70U", "Jet50U", "Jet30U", "Jet15\_HNF" ]
	hist_labels = ["Jet140U", "Jet100U", "Jet70U", "Jet50U", "Jet30U", "Jet15U_HcalNoiseFiltered" ]
	lower_pTs = [140, 100, 70, 50, 30, 15]


	for i in range(len(hist_labels)):
		
		hist = normalize_hist( mod_hists[hist_labels[i]].hist() )
		# hist = mod_hists[hist_labels[i]].hist()

		n_bins = hist.nbins()

		# Loop through those bins.
		for j in range(n_bins):
			current_bin_x = hist.GetBinCenter(j)
			current_bin_y = hist.GetBinContent(j),
			# print 
			if current_bin_x < lower_pTs[i]:
				hist.SetBinContent(j, 0.)


		hist.SetColor(colors[i])
		hist.SetTitle(labels[i])

		rplt.errorbar(hist, emptybins=False, xerr=1, yerr=1, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)


	# Info about R, pT_cut, etc.
	extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
	handles = [extra]
	labels = ["$ \\textrm{Anti--}k_{t}\\textrm{:}~R = 0.5$\n$\eta<2.4$"]
	info_legend = plt.gca().legend(handles, labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.56])
	plt.gca().add_artist(info_legend)


	plt.gca().set_xlabel("Trigger Jet $p_T$ (GeV)", fontsize=60, labelpad=50)
	plt.gca().set_ylabel("A.U.", rotation=0, fontsize=60, labelpad=65)

	plt.gca().add_artist(logo_box())

	plt.gca().xaxis.set_minor_locator(MultipleLocator(10))
	plt.gca().set_yscale('log')

	handles, labels = plt.gca().get_legend_handles_labels()
	legend = plt.legend(handles[::-1], labels[::-1], frameon=0, bbox_to_anchor=[0.97, 0.99])
	ax = plt.gca().add_artist(legend)


	plt.autoscale()
	
	plt.tick_params(which='major', width=5, length=25, labelsize=50)
	plt.tick_params(which='minor', width=3, length=15)

	plt.gcf().set_size_inches(30, 24, forward=1)

	plt.savefig(default_dir + "trigger_turn_on_curves.pdf")

	plt.clf()





def trigger_efficiency_plot():
	mod_hists = parsed_linear[0]

	colors = ['green', 'magenta', 'blue', 'red', 'brown', 'orange']
	labels = ["Jet140U / 100U", "Jet100U / 70U", "Jet70U / 50U", "Jet50U / 30U", "Jet30U / 15U\_HNF", "" ]
	hist_labels = [("Jet140U", "Jet100U"), ("Jet100U", "Jet70U"), ("Jet70U", "Jet50U"), ("Jet50U", "Jet30U"), ("Jet30U", "Jet15U_HcalNoiseFiltered") ]
	lower_pTs = [140, 100, 70, 50, 30, 15]

	# rplt.hist(mod_hists[0].hist())

	for i in range(len(hist_labels) ):
		
		first_hist, second_hist = mod_hists[hist_labels[i][0]], mod_hists[hist_labels[i][1]]

		ratio_hist = first_hist.hist() / second_hist.hist()

		ratio_hist.SetColor(colors[i])
		ratio_hist.SetTitle(labels[i])

		rplt.errorbar(ratio_hist, emptybins=False, xerr=1, yerr=1, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)

	
	# Info about R, pT_cut, etc.
	extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
	handles = [extra]
	labels = ["$ \\textrm{Anti--}k_{t}\\textrm{:}~R = 0.5$\n$\eta<2.4$"]
	info_legend = plt.gca().legend(handles, labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.33, 0.80])
	plt.gca().add_artist(info_legend)


	plt.gca().set_xlabel("Trigger Jet $p_T$ (GeV)", fontsize=60, labelpad=50)
	plt.gca().set_ylabel("A.U.", rotation=0, fontsize=60, labelpad=65)

	plt.gca().add_artist(logo_box())

	plt.gca().xaxis.set_minor_locator(MultipleLocator(10))
	plt.gca().set_yscale('log')

	handles, labels = plt.gca().get_legend_handles_labels()
	legend = plt.legend(handles[::-1], labels[::-1], frameon=0, bbox_to_anchor=[0.99, 0.99])
	ax = plt.gca().add_artist(legend)


	plt.autoscale()
	
	plt.tick_params(which='major', width=5, length=25, labelsize=50)
	plt.tick_params(which='minor', width=3, length=15)

	plt.gcf().set_size_inches(30, 24, forward=1)
	plt.savefig(default_dir + "trigger_efficiency.pdf")

	plt.clf()




start = time.time()


# trigger_turn_on_curves()

trigger_efficiency_plot()

end = time.time()

print "Finished all plotting in {} seconds.".format(end - start)