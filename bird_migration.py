import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

bird_data = pd.read_csv('docs/bird_tracking.csv')
bird_names = bird_data['bird_name'].unique()
bird_data['date_time'] = pd.to_datetime(bird_data['date_time'])
bird_data['date'] = bird_data['date_time'].dt.date
grouped_bird_data = bird_data.groupby(['bird_name', 'date'])

plt.figure(figsize=(6, 6))
ax = plt.axes(projection=ccrs.Mercator())
ax.set_extent((-25, 20, 52, 10))
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
for name in bird_names:
    ix = bird_data['bird_name'] == name
    x, y = bird_data['longitude'][ix], bird_data['latitude'][ix]
    plt.plot(x, y, '.', transform=ccrs.Geodetic(), label=name)
plt.title("Bird Routes")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc='upper left')
plt.savefig('plots/bird_migration_1')

plt.figure(figsize=(10, 4))
for name in bird_names:
    ix = bird_data['bird_name'] == name
    bird_data['speed_2d'][ix].plot(kind='hist',
                                   histtype='step',
                                   bins=np.linspace(0, 20, 20),
                                   normed=True,
                                   label=name)
plt.title("Speed Histogram")
plt.xlabel("2D speed (m/s)")
plt.ylabel("Frequency")
plt.legend()
plt.savefig('plots/bird_migration_2')

plt.figure(figsize=(8, 4))
for name in bird_names:
    times = bird_data['date_time'][bird_data['bird_name'] == name]
    times = times.reset_index(drop=True)
    elapsed_time = np.array([t - times[0] for t in times])
    plt.plot(elapsed_time / datetime.timedelta(days=1), label=name)
plt.title("Observation Frequency")
plt.xlabel("Observation")
plt.ylabel("Elapsed time (days)")
plt.legend()
plt.savefig('plots/bird_migration_3')

plt.figure(figsize=(10, 4))
for name in bird_names:
    grouped_bird_data.speed_2d.mean()[name].plot(label=name)
plt.title("Mean Speeds")
plt.xlabel("Day")
plt.ylabel("Mean speed (m/s)")
plt.legend(loc='upper left')
plt.savefig('plots/bird_migration_4')

plt.show()
