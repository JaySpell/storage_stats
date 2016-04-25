from bokeh.plotting import *
from numpy import pi
import parse_utils

def graph_it():
    output_file("test.html")
    p = figure(plot_width=400, plot_height=400)
    p.line([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], line_width=2)
    show(p)

def pie_it(percents, starts, ends):
    # define starts/ends for wedges from percentages of a circle

    #percents = [0, 0.3, 0.4, 0.6, 0.9, 1]

    #Get list of storage stats
    storage_stats = paruse_utils.group_totals(['tmcv7000-4', 'tmcv7000-3'])

    #Get totals and convert to %
    percents = parse_utils.space_percent(storage_stats, sel_out="list")
    percents.append(1)

    #Get list instead of dict
    starts = [p*2*pi for p in percents[:-1]]
    ends = [p*2*pi for p in percents[1:]]

    # a color for each pie piece
    colors = ["red", "green", "blue", "orange", "yellow"]

    p = figure(x_range=(-1,1), y_range=(-1,1))

    p.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors)

    # display/save everythin
    output_file("pie.html")
    show(p)
