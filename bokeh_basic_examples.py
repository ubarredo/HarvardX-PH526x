from itertools import product

import numpy as np
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show

output_file('plots/bokeh_basic_examples_1.html', title="Rect Example")
plot_values = [1, 2, 3, 4, 5]
plot_colors = ['blue', 'red', 'green', 'orange']
grid = list(product(plot_values, plot_values))
xs, ys = zip(*grid)
colors = [plot_colors[i % 4] for i in range(len(grid))]
alphas = np.linspace(0, 1, len(grid))
plot_source = ColumnDataSource(data={'x': xs,
                                     'y': ys,
                                     'colors': colors,
                                     'alphas': alphas})
fig = figure(tools='resize, hover, save')
fig.rect('x', 'y',
         width=0.9, height=0.9,
         source=plot_source,
         color='colors', alpha='alphas')
hover = fig.select(dict(type=HoverTool))
hover.tooltips = {"Value": "@x, @y, @colors"}
show(fig)

output_file('plots/bokeh_basic_examples_2.html', title="Spatial Example")
points = [(0, 0), (1, 2), (3, 1)]
xs, ys = zip(*points)
colors = ['red', 'blue', 'green']
location_source = ColumnDataSource(data={'x': xs,
                                         'y': ys,
                                         'colors': colors})
fig = figure(title="Title",
             x_axis_location='above',
             tools='resize, hover, save')
fig.plot_width = 300
fig.plot_height = 380
fig.circle('x', 'y',
           size=10,
           source=location_source,
           color='colors',
           line_color=None)
hover = fig.select(dict(type=HoverTool))
hover.tooltips = {"Location": "(@x, @y)"}
show(fig)
