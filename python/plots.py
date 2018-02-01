from __future__ import division

import math
import time
import sys
import hists


from MODPlot import *


import parse
import pfc_parse



def compile_sources(parsed_hists):

    compilation = []

    for k in range(len(parsed_hists)):

        compilation.append(parsed_hists[k])

    return compilation


def compile_hists(var, parsed_hists, x_scale='linear'):

    compilation = []

    max_index = len(parsed_hists[0][var])

    for i in range(max_index):

        sub_list = []

        for k in range(len(parsed_hists)):

            sub_list.append(parsed_hists[k][var][i])
            
        compilation.append(sub_list)

    return compilation

default_dir = "plots/Version 1/"

start = time.time()

# Make sure you have run ./python/parse.py first
parsed_linear = parse.load_root_files_to_hist(log=False)
parsed_hists = compile_sources(parsed_linear)

parsed_log = parse.load_root_files_to_hist(log=True)
parsed_log_hists = compile_sources(parsed_log)

# Uncomment to load PFC hists. Make sure you have run ./python/pfc_parse.py first
# parsed_pfc = pfc_parse.load_pfc_root_files_to_hist()
# parsed_pfc_hists = compile_sources(parsed_pfc)



end = time.time()


print "Finished parsing all files in {} seconds. Now plotting them!".format(end - start)


start = time.time()

# LINEAR PLOTS
create_multi_page_plot(filename=default_dir + "multiplicity_all_linear.pdf", 
                       hists=compile_hists('multiplicity', parsed_hists))
create_multi_page_plot(filename=default_dir + "mul_pre_SD_all_linear.pdf", 
                       hists=compile_hists('mul_pre_SD', parsed_hists))

create_multi_page_plot(filename=default_dir + "hardest_jet_phi_all_linear.pdf",
                        hists=compile_hists('hardest_phi', parsed_hists))
create_multi_page_plot(filename=default_dir + "hardest_jet_eta_all_linear.pdf",
                       hists=compile_hists('hardest_eta', parsed_hists))

# LOGARITHMIC PLOTS
create_multi_page_plot(filename=default_dir + "basic_sub_pTD_track_log.pdf",
                        hists=compile_hists('track_pT_D_pre_SD', parsed_log_hists,
                                           x_scale='log'), x_scale='log')
create_multi_page_plot(filename=default_dir + "basic_sub_lha_all_log.pdf",
                        hists=compile_hists('LHA_pre_SD', parsed_log_hists), x_scale='log')
create_multi_page_plot(filename=default_dir + "basic_sub_lha_track_log.pdf",
                       hists=compile_hists(
                           'track_LHA_pre_SD', parsed_log_hists),
                       x_scale='log')

# PFC PLOTS
# create_multi_page_plot(filename=default_dir + "pfc_pT.pdf", 
#                        hists=compile_hists('pfc_pT', parsed_pfc_hists))
# create_multi_page_plot(filename=default_dir + "pfc_eta.pdf",
#                        hists=compile_hists('pfc_eta', parsed_pfc_hists))




end = time.time()
print "Finished all plotting in {} seconds.".format(end - start)
