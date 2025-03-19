import numpy as np
import pandas as pd
from pandas import Timestamp 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import griddata
import time

grid_size = 1000
fig,ax = plt.subplots()

# Inverse Distance Weighting function
def idw_interpolation(x, y, dcs, grid_x, grid_y, ts, power=2):

    weights = np.zeros_like(grid_x, dtype=float)
    values_grid = np.zeros_like(grid_x, dtype=float)
    
    for i in range(len(x)):
        dists = np.sqrt((grid_x - x[i])**2 + (grid_y - y[i])**2)
        dists[dists == 0] = 1e-10  # Avoid division by zero
        w = 1 / (dists ** power)

        weights += w
        values_grid += w * dcs[i][ts]['Temperature   (°C)']
    
    return values_grid / weights

# Hardcoded sensor location data

sensor_positions = {
    'sensor1': (100, 200),
    'sensor2': (800, 900),
    'sensor3': (150, 750),
    'sensor4': (400, 350),
    'sensor5': (350, 850)
}

sensor_values= {
   # 'sensor1': {}
   # 'sensor2': {}
   # 'sensor3': {}
   # 'sensor4': {}
   # 'sensor5': {}
}
df1 = pd.read_csv('sensor1.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df2 = pd.read_csv('sensor2.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df3 = pd.read_csv('sensor3.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df4 = pd.read_csv('sensor4.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df5 = pd.read_csv('sensor5.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
dfs = [df1,df2,df3,df4,df5]
#print(df1)
#print(df1.columns.tolist())
timestamps = df1['Date-Time'].to_list()
#print(timestamps)
dcs = []
for df in dfs:
    df = df.set_index('Date-Time')
    dc = df.to_dict('index')
    #print(df)
    dcs.append(dc)

frames = {}
heatmaps = []
mask = np.zeros((grid_size, grid_size), dtype=bool)
# Prepare grid
grid_x, grid_y = np.meshgrid(np.linspace(0, grid_size, grid_size), np.linspace(0, grid_size, grid_size))

# Extract sensor locations
sensor_x = np.array([sensor_positions[key][0] for key in sensor_positions])
sensor_y = np.array([sensor_positions[key][1] for key in sensor_positions])

# Perform IDW interpolation
for ts in timestamps:
    heatmaps.append(idw_interpolation(sensor_x, sensor_y, dcs, grid_x, grid_y, ts))
ims= []
#for i in range(len(heatmaps)):
 #   im = ax.imshow(heatmaps[i], extent=(0, grid_size, 0, grid_size), origin='lower', cmap='plasma', alpha=1.0)
    #im = ax.scatter(sensor_x, sensor_y, c='blue', edgecolors='black', label='Sensors')
 #   ims.append([im])
im = ax.imshow(heatmaps[0], extent=(0, grid_size, 0, grid_size), origin='lower', cmap='plasma', alpha=1.0)
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Temperature (°C)')

# Add axis labels
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")

sensor_plot = ax.scatter(sensor_x, sensor_y, c='blue', edgecolors='black', label='Sensors')

#sensor_labels = [ax.text(sensor_x[i] + 2, sensor_y[i] + 2, f"{sensor_temps[0][i]:.1f}°C", 
#                         color='white', fontsize=10, ha='left', va='bottom', bbox=dict(facecolor='black', alpha=0.5))
#                 for i in range(len(sensor_x))]


def next_frame(frame):
    im.set_array(heatmaps[frame])
    ax.set_title(f"Cave Temperature at {timestamps[frame]}")  # This isnt working
    print(timestamps[frame])
    sensor_plot = ax.scatter(sensor_x, sensor_y, c='blue', edgecolors='black', label='Sensors')
    return im, sensor_plot


ani = animation.FuncAnimation(fig, next_frame, frames=len(heatmaps), interval=5, blit=True,
                                repeat_delay=1000)
# Plot the heatmap
#plt.colorbar(label='Temperature (°C)')
#plt.legend()
#plt.title('Cave Temperature Heatmap')
#plt.xlabel('X Position')
#plt.ylabel('Y Position')

plt.show()
