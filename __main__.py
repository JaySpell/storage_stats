from bokeh.plotting import figure, output_file, show

def graph_it():
    output_file("test.html")
    p = figure(plot_width=400, plot_height=400)
    p.line([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], line_width=2)
    show(p)
