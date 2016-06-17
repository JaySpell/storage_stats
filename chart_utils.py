from bokeh.plotting import *
from bokeh.models import *
from numpy import pi
from bokeh.charts import Donut, show, output_file
from bokeh.charts.utils import df_from_json
import pandas as pd
import numpy as np
import datetime
from bokeh.embed import components

def piechart(percents, **kwargs):
    plot = None
    chart_title = kwargs.get('title', 'Default Chart')

    # create a figure and add a wedge glyph to it
    plot = figure(title=chart_title,
                toolbar_location=None,
                x_range=(-1, 1.1),
                y_range=(-1, 1.1),
                min_border=10,
                min_border_left=50,
                title_text_font_size='12pt',
                width=450,
                height=450)
    plot.outline_line_width = 0
    plot.outline_line_color = "white"
    plot.xaxis.visible = None
    plot.xgrid.grid_line_color = None
    plot.yaxis.visible = None
    plot.ygrid.grid_line_color = None
    total = percents.pop('space')[0]
    colors = ["#726F78", "#5350C5"]
    wedges = []
    wedge_sum = 0

    if not total == 0:
        for i, (key, val) in enumerate(percents.iteritems()):
            wedge = {}
            wedge['start'] = 2*pi*wedge_sum
            wedge_sum = (val) + wedge_sum
            wedge['end'] = 2*pi*wedge_sum
            wedge['name'] = '{:.40} ({:.2f} %)'.format(key, val*100)
            wedge['color'] = colors[i%len(colors)]
            wedges.append(wedge)

    plot._renderers = []
    for i, wedge in enumerate(wedges):
        plot.wedge(x=0, y=0, radius=0.75,
                   legend=wedge['name'],
                   start_angle=wedge['start'],
                   end_angle=wedge['end'],
                   color=wedge['color'],
                   line_color='white',
                   radius_units='data')
    plot.legend.glyph_width = 10
    file_name = chart_title.replace(' ', '') + ".html"
    output_file(file_name)
    save(plot)

def donutchart(*args, **kwargs):
    #get info from submitted data
    data = kwargs.get('data', 'None')
    ids = kwargs.get('ids', 'None')
    vals = kwargs.get('vals', 'None')
    val_name = kwargs.get('val_name', 'None')
    v_name = kwargs.get('v_name', 'None')
    out_file = kwargs.get('out_file', 'None')

    if vals or data or ids or val_name == 'None':
        return "Data must be submitted"

    df = df_from_json(data)
    df = df.sort("total", ascending=False)
    df = pd.melt(df, id_vars=[ids],
                value_vars=[vals],
                value_name=val_name,
                var_name=v_name)
    d = Donut(df, label=[ids, v_name],
            values=v_name,
            text_font_size='8pt',
            hover_text='vals')

    output_file(out_file)
    save(d)

def growthchart(tiername, dates, used, *args, **kwargs):
    plot = figure(tools="pan, wheel_zoom, box_zoom, resize, save",
                plot_width=900,
                plot_height=600,
                toolbar_location="above",
                x_axis_type="datetime")
    plot.title = "One Year of Growth: " + tiername
    plot.grid.grid_line_alpha = 0.5
    plot.xaxis.axis_label = 'Month'
    plot.yaxis.axis_label = 'Space in TB'
    plot.line(dates, used, color="#5350C5", line_width=2)
    plot.ygrid.grid_line_color = "#726F78"
    plot.ygrid.grid_line_dash = [6, 4]
    plot.ygrid.grid_line_alpha = 0.5
    plot.xgrid.grid_line_color = None


    output_file("/home/kcup/python/graph/growth_" + tiername + ".html",
        title="growth")

    plots = (plot)
    script, div = components(plots)

    return script, div
