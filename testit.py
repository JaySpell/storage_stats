from bokeh.plotting import *
from bokeh.models import *
from numpy import pi
import parse_utils

group_list = ['tmcv7000-4', 'tmcv7000-3']

def pie_it(percents):
    #Get list of storage stats
    chart_title = "Total Space - Tmcsvc02"
    storage_stats = parse_utils.group_totals(['tmcv7000-4', 'tmcv7000-3'])

    #Get totals and convert to %
    percents = parse_utils.space_percent(storage_stats, sel_out="list")
    percents.append(1)
    percents.insert(0, 0)
    print(percents)

    starts = [p*2*pi for p in percents[:-1]]
    ends = [p*2*pi for p in percents[1:]]

    # a color for each pie piece
    colors = ["#16CC62", "#63667F"]

    p = figure(x_range=(-1,1),
            y_range=(-1,1),
            title=chart_title)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.wedge(x=0, y=0, radius=1,
            start_angle=starts, end_angle=ends,
            color=colors,
            legend="tmcv7000-4")
    p.text(text="tmcv7000-4, tmcv7000-3")
    p.legend.orientation = "bottom_left"

    # display/save everythin
    output_file("pie.html")
    show(p)

def piechart(percents, **kwargs):
    plot = None
    chart_title = kwargs.get('title', 'Default Chart')

    # create a figure and add a wedge glyph to it
    plot = figure(title=chart_title,
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
    print total
    print(percents)

    colors = ["#FF2F27", "#0B75CC"]
    wedges = []
    wedge_sum = 0
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
    output_file("pie.html")
    show(plot)

if __name__ == "__main__":
    # Setup Charts
    percents = {'test1': 10, 'test2': 32, 'test3': 18, 'test4': 144}
    #piechart(percents)

    a_dict = parse_utils.group_totals(group_list)
    b = parse_utils.space_percent(a_dict)
    print(b)
    title = 'Tier 1'
    piechart(b, title='Tier 1')
