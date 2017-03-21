import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show
from sklearn.cluster.bicluster import SpectralCoclustering

data = pd.read_csv('docs/whiskies.txt')
data['Region'] = pd.read_csv('docs/regions.txt')

correlations = np.array(data.iloc[:, 2:14].transpose().corr())
plt.figure(figsize=(10, 4))
plt.subplot(121)
plt.title("Original")
plt.pcolor(correlations, cmap='inferno')
plt.colorbar()

model = SpectralCoclustering(n_clusters=6, random_state=0)
model.fit(correlations)
data['Group'] = model.row_labels_
data = data.ix[np.argsort(model.row_labels_)]
data = data.reset_index(drop=True)
correlations = correlations[np.argsort(model.row_labels_), :]
correlations = correlations[:, np.argsort(model.row_labels_)]
plt.subplot(122)
plt.title("Rearranged")
plt.pcolor(correlations, cmap='inferno')
plt.colorbar()
plt.savefig('plots/classifying_whiskies_1')

group_colors = ['red', 'yellow', 'green', 'blue', 'purple', 'orange']
correlation_colors = []
for i in range(len(correlations)):
    for j in range(len(correlations)):
        if correlations[i, j] < 0.7:
            correlation_colors.append('white')
        elif data['Group'][i] == data['Group'][j]:
            correlation_colors.append(group_colors[data['Group'][i]])
        else:
            correlation_colors.append('lightgray')

distilleries = list(data['Distillery'])
output_file('plots/classifying_whiskies_2.html', title="Whisky Correlations")
plot_source = ColumnDataSource(
    data={'x': np.repeat(distilleries, len(distilleries)),
          'y': distilleries * len(distilleries),
          'colors': correlation_colors,
          'alphas': correlations.flatten(),
          'correlations': correlations.flatten()})
fig = figure(title="Whisky Correlations",
             x_axis_location='above',
             tools='resize, hover, save',
             x_range=list(reversed(distilleries)),
             y_range=distilleries)
fig.grid.grid_line_color = None
fig.axis.axis_line_color = None
fig.axis.major_tick_line_color = None
fig.axis.major_label_text_font_size = '5pt'
fig.xaxis.major_label_orientation = 1
fig.rect('x', 'y',
         .9, .9,
         source=plot_source,
         color='colors',
         alpha='alphas')
hover = fig.select(dict(type=HoverTool))
hover.tooltips = {"Whiskies": "@x, @y",
                  "Correlation": "@correlations"}
show(fig)

region_colors = dict(zip(data['Region'].unique(), group_colors))
r_colorlist = [region_colors[i] for i in data['Region']]
g_colorlist = [group_colors[i] for i in data['Group']]
plot_n = 3
for title, colorlist in [("Locations & Regions", r_colorlist),
                         ("Locations & Groups", g_colorlist)]:
    output_file('plots/classifying_whiskies_%s.html' % str(plot_n))
    plot_n += 1
    plot_source = ColumnDataSource(
        data={'x': data['Latitude'],
              'y': data['Longitude'],
              'colors': colorlist,
              'regions': data['Region'],
              'distilleries': distilleries})
    fig = figure(title=title,
                 x_axis_location='above',
                 tools='resize, hover, save')
    fig.plot_width = 400
    fig.plot_height = 500
    fig.circle('x', 'y',
               size=9,
               source=plot_source,
               color='colors',
               line_color='black')
    fig.xaxis.major_label_orientation = 1
    hover = fig.select(dict(type=HoverTool))
    hover.tooltips = {"Distillery": "@distilleries",
                      "Location": "(@x, @y)"}
    show(fig)

plt.show()
