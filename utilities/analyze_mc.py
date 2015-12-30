from subprocess import call
import os
from time import time
import sys
from collections import defaultdict


def run_analyzer():
	
	location = "/home/aashish/MODMonteCarlo/data/"
	# all_mc = ["pythia", "herwig", "sherpa"]
	all_mc = ["herwig", "sherpa"]

	call(['make'])

	for mc in all_mc:

		# call(['rm', "/home/aashish/" + mc + "_truth.dat"])
		# call(['rm', "/home/aashish/" + mc + "_reco.dat"])

		call(['./bin/analyze', location + mc + "_truth.mod", "/home/aashish/pythia/" + mc + "_truth.dat"])
		call(['./bin/analyze', location + mc + "_reco.mod", "/home/aashish/pythia/" + mc + "_reco.dat"])


start = time()

run_analyzer()

end = time()

print "Everything done in " + str(end - start) + " seconds!"