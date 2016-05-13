from bokeh.plotting import *
from bokeh.models import *
from numpy import pi


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
                title_text_font_size='12pt')
    plot.xaxis.visible = None
    plot.xgrid.grid_line_color = None
    plot.yaxis.visible = None
    plot.ygrid.grid_line_color = None
    total = percents.pop('space')[0]
    colors = ["#F84337", "#5350C5"]
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
        plot.wedge(x=0, y=0, radius=1,
                   legend=wedge['name'],
                   start_angle=wedge['start'],
                   end_angle=wedge['end'],
                   color=wedge['color'],
                   line_color='white',
                   radius_units='data')
    plot.legend.glyph_width = 10
    file_name = chart_title + ".html"
    output_file(file_name)
    save(plot)
