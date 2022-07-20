#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Dumbledraw.dumbledraw as dd
import Dumbledraw.rootfile_parser_inputshapes as rootfile_parser
import Dumbledraw.styles as styles
import ROOT as R

import argparse
from copy import deepcopy

from root_numpy import hist2array
import numpy as np
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger("")


def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Produce shapes for 2016 Standard Model analysis.")
    parser.add_argument(
        "--channels",
        default=[],
        nargs='+',
        type=str,
        help="Channels to be considered.")
    parser.add_argument(
        "--categories",
        default=[],
        nargs='+',
        type=str,
        help="Categories to be considered.")
    parser.add_argument(
        "--variables",
        default=[],
        nargs='+',
        type=str,
        help="Variables to be considered.")
    return parser.parse_args()

#xlabels = { "pt": r'Reconstructed p_{T}^{H} (GeV)', "eta":r'Reconstructed #eta',"phi": r' Reconstructed #phi',"m":r'Reconstructed mass m_{H} (GeV)'}

def main(args):
	hack = []
	roc = {}
	shapes = {}
	for channel in args.channels:
		roc[channel] = {}
		shapes[channel] = {}
		for category in args.categories:
			roc[channel][category] = {}
			shapes[channel][category] = {}
	for variable in args.variables:
		for channel in args.channels:
			for category in args.categories:
				rootfile = rootfile_parser.Rootfile_parser("2016_shapes.root", "smhtt", "Run2016", variable, 125)
				#print rootfile.list_contents()
				name = "_".join([channel, category])
				out_name = "_".join([channel, category, variable])
				print name	
	
				# create canvas:
				#   First argument defines subplot structure: List of splits from top to bottom (max. 1.0 to min. 0.0). A split can be a single position or a pair resulting in gap.
				#   Further arguments set general style.
				plot = dd.Plot(
					[0.05], "ModTDR", r=0.04, l=0.14)
	
				#bkg_processes = ["EWK", "QCD", "VV", "W", "TTT", "TTJ", "ZJ", "ZL", "ZTT"]
				bkg_processes = ["EWK", "QCD", "VV", "W", "TTT", "TTJ", "ZL", "ZJ", "ZTT"]
				if channel == 'tt':
					bkg_processes = ["QCD", "VVT", "VVJ", "W", "TTT", "TTJ", "ZL", "ZJ", "ZTT"]
	
				# register histograms in the subplots (can be done globally or for specific subplots). regustered histograms are not necessarily plotted later.
				for process in bkg_processes:
					plot.add_hist(
						rootfile.get(channel, name, process), process, "bkg"
					)  # get(channel, category, process) and assign specific name and group name to histogram. The group name is optional.
					plot.setGraphStyle(
						process, "hist", fillcolor=styles.color_dict[process])

#				for i in range(1):
#					plot.add_hist(
#						rootfile.get(channel, name, "ggh"), "ggh"
#						)  # signal histograms are used twice in order to realize a two color line style
#					plot.add_hist(
#						rootfile.get(channel, name, "ggh"), "ggh_top")
#					plot.add_hist(rootfile.get(channel, name, "qqH"), "qqH")
#					plot.add_hist(
#						rootfile.get(channel, name, "qqH"), "qqH_top")
				plot.add_hist(rootfile.get(channel, name, "data_obs"), "data_obs", "data_obs")
				# set some graph styles
#				plot.setGraphStyle(
#					"ggh", "hist", linecolor=styles.color_dict["ggh"], linewidth=3)
#				plot.setGraphStyle("ggh_top", "hist", linecolor=0)
#				plot.setGraphStyle(
#					"qqH", "hist", linecolor=styles.color_dict["qqH"], linewidth=3)

#				plot.setGraphStyle("qqH_top", "hist", linecolor=0)
				plot.setGraphStyle(
					"data_obs",
					"e0",
					markersize=1,
					fillcolor=styles.color_dict["unc"],
					linecolor=1)
				plot.create_stack(bkg_processes, "stack")
#				plot.subplot(1).normalize(["data_obs"], bkg_processes) # would also work but add up the single bkg histograms in the background
				if channel == 'tt':
					plot.subplot(0).setYlims(1, 1e5)
					plot.DrawChannelCategoryLabel("#tau_{h}#tau_{h}")
				elif channel == 'mt':
					plot.subplot(0).setYlims(1, 1e7)
					plot.DrawChannelCategoryLabel("#mu#tau_{h}")
				elif channel == 'et':
					plot.subplot(0).setYlims(0.1, 1e7)
					plot.DrawChannelCategoryLabel("e#tau_{h}")

	#			plot.subplot(0).setXlims(-200, 200)
	#			plot.subplot(1).setXlims(-200, )
				plot.subplot(1).setYlims(0, 2)
				plot.subplot(0).setLogY()
				plot.subplot(0).setXlabel(variable)
				plot.subplot(0).setYlabel("N_{events}")
				plot.subplot(1).setYlabel("ratio to bkg")
				plot.scaleXTitleSize(0.8)
				plot.scaleXLabelSize(0.8)
				plot.scaleYTitleSize(0.8)
				plot.scaleYLabelSize(0.8)
				plot.scaleXLabelOffset(2.0)
				plot.scaleYTitleOffset(1.1)
				plot.subplot(0).Draw(['stack', "data_obs", 
										"ggh", "qqH", "ggh_top", "qqH_top", ])
	#			plot.subplot(1).add_hist(R.TF1("line", "1", 0, 1000), "line")
#				plot.subplot(1).Draw(["data_obs", "line"])
	
				# create legends
				bkg_processes.reverse()
				suffix = ["", "_top"]
				for i in range(2):
					plot.add_legend(width=0.5, height=0.08)
					for process in bkg_processes:
						plot.legend(i).add_entry(0, process,
												 styles.legend_label_dict[process], 'f')
					#plot.legend(i).add_entry(1, "ggh%s" % suffix[i], "ggh", 'l')
					#plot.legend(i).add_entry(1, "qqH%s" % suffix[i], "qqH", 'l')
#					plot.legend(i).add_entry(0, "data_obs", "Data", 'PE')
					plot.legend(i).setNColumns(3)
				plot.legend(0).Draw()
				plot.subplot(1)._pad.SetGrid()
	
				# draw additional labels
				plot.DrawCMS()
				plot.DrawLumi("35.9 fb^{-1} (13 TeV)")
	
				# save plot
				plot.save(out_name + ".png")
				plot.save(out_name + ".pdf")
				hack.append(plot)



if __name__ == "__main__":
    args = parse_arguments()
    setup_logging("plot_shapes.log", logging.INFO)
    main(args)
