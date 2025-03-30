import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
import os
import subprocess
import heapq
import math


def get_mask(path="output_list.txt"):
   
    mask_array = np.load('my_array.npy')
    print(type(mask_array))
    print(mask_array)
    print("Got mask from file, shape:", mask_array.shape)
    return mask_array

def load_cave_map(image_path):
    cave_map = Image.open(image_path)
    return np.array(cave_map)

def get_dist(c, sc):  ## straight line  
    x,y,sx,sy=c[0],c[1],sc[0],sc[1]
    if x == sx and y == sy:
        return 1e-10
    else:
        a = math.pow(x-sx,2)
        b = math.pow(y-sy,2)
        value = math.sqrt(a+b)
        return value

def dijkstras(start, mask):
    cols, rows = mask.shape
    distances = {start: 0}  # Stores shortest distance to each point
    priority_queue = [(0, start)]  # (cost, (x, y))
    print("ENTERED ASTAR with + " + str(start))
    count = 0
    count_if_one = 0
    count_if_two = 0
    i=0
    while priority_queue:
        cost, (x, y) = heapq.heappop(priority_queue)

        ##
        ## EDGE CASE ERRORS HERE ?? 
        ##
        
        for direction in DIRECTIONS:
            i += 1
            nx, ny = x + direction[0], y + direction[1]

            if 0 <= nx < rows and 0 <= ny < cols and mask[ny][nx] == 1:
               
                new_cost = distances[(x, y)] + (1 if abs(direction[0]) + abs(direction[1]) == 1 else math.sqrt(2))

                if new_cost < distances.get((nx, ny), float('inf')):
                    distances[(nx, ny)] = new_cost
                    heapq.heappush(priority_queue, (new_cost, (nx, ny))) 
    return distances

def idw_interpolation(sx, sy, dcs, grid_x, ts, mask, sensor_distances_astar, alpha=1, mode = 0):
    # Create output arrays, initializing with NaN
    top = np.full_like(grid_x, np.nan, dtype=float)
    bottom = np.full_like(grid_x, np.nan, dtype=float)

    # This is where optimization needs to happen if we are gonna try
    for rows in range(grid_x.shape[1]-1):
        for cols in range(grid_x.shape[0]-1):

            if mask[cols][rows] == 1:
                top[cols][rows],bottom[cols][rows] = 0,0              
                for i in range(len(sx)):
                    eps = 1e-10
                    if mode == 0:
                        d = max(get_dist((cols, rows), (sx[i], sy[i])), eps) ** alpha
                    elif mode == 1:
                        target_pos = (rows, cols)
                        distance = sensor_distances_astar[sensor_names[i]][target_pos]
                        d = max(distance, eps) ** alpha

                    top[cols][rows] += dcs[i][ts]['Temperature   (°C)'] / d  #### USING HARDCODED KEY HERE
                    bottom[cols][rows] += 1/d

    return top/bottom

def get_heatmaps_file():
    heatmaps = []
    for filename in sorted(os.listdir(output_dir_heatmaps)):  # Ensure files are loaded in order
        if filename.endswith(".npz"):
            data = np.load(os.path.join(output_dir_heatmaps, filename))  # Load .npz file
            heatmap = data["arr_0"].astype(np.float32)  # Convert to float32
            heatmaps.append(heatmap)
    return heatmaps

def save_heatmaps_npz(heatmaps):
    """Saves a list of NumPy arrays to a .npz file."""
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

    for i, heatmap in enumerate(heatmaps):
        np.savez_compressed(f"{output_dir_heatmaps}/heatmap_{i:04d}.npz", heatmap)  # Save each frame

def get_heatmaps(start=0, end=100, skip=1, distances=[], alpha = 1, mode = 0):
    i = 1
    heatmaps = []
    for ts in timestamps[start:end:skip]:    ########## calc a heatmap for every nth timestamp 
        print("Heatmap -- " + str(i))
        i +=1
        max = 0
        heatmap = idw_interpolation(sensor_x, sensor_y, dcs, grid_x, ts, mask, distances, alpha, mode)
        heatmaps.append(heatmap)
    save_heatmaps_npz(heatmaps)
    return heatmaps

def get_s_dev(heatmaps):
    all_values = np.concatenate([hm[~np.isnan(hm)].flatten() for hm in heatmaps])  
    avg = np.mean(all_values) a
    top = 0
    for val in all_values:
        top += math.pow(val - avg,2)
    final = math.sqrt(top/all_values.size)
    return final , avg

def save_heatmaps_png(heatmaps, sensor_x, sensor_y, cave_map, x_size, y_size, timestamps, output_dir):
    os.makedirs(output_dir, exist_ok=True)  
    s_dev = get_s_dev(heatmaps)
    print("Standard Deviation is ... " + str(s_dev[0]))
    vmin = s_dev[1] - (s_dev[0]*2)
    vmax = s_dev[1] + (s_dev[0]*2)
    print(f"Using vmin={vmin}, vmax={vmax} for color mapping")
    i = 0

    for heatmap in heatmaps[::1]:
        print(f"Saving frame {i+1}/{len(heatmaps)}")
       
        fig,ax = plt.subplots(figsize=(x_size / 100, y_size / 100))
        ax.imshow(cave_map, extent=[0, x_size, 0, y_size], cmap='Greys')
        im = ax.imshow(heatmap, extent=(0, x_size, 0, y_size), origin='lower', cmap=c_map, vmin=vmin, vmax=vmax)
        cbar = fig.colorbar(im, ax=ax, extend='both')
        cbar.set_label('Temperature (°C)', fontsize = 20)
        cbar.cmap.set_over('magenta')
        cbar.cmap.set_under('blueviolet')
        ax.set_title(f"Cave Temperature at {timestamps[i]}", fontsize=25)  
        ax.set_xlabel("X Position", fontsize=20)
        ax.set_ylabel("Y Position", fontsize=20)
        j=0
        for x, y in zip(sensor_x, sensor_y):  
            ax.text(x, y, "Sensor: "+str(j), fontsize=15, color="white", ha="center", va="bottom",
                    bbox=dict(facecolor='black', edgecolor='none', alpha=0.5, pad=1))
            j+=1

        ax.scatter(sensor_x, sensor_y, c='green', edgecolors='black', label='Sensors')

        frame_filename = f"{output_dir}/frame_{i:04d}.png"
        plt.savefig(frame_filename, bbox_inches="tight", pad_inches=0, dpi=100)
        plt.close(fig)  # Free memory by closing the figure
        print(f"Saved {frame_filename}")
        i += 1

def generate_video_from_pngs(output_dir="frames", output_video="output_movie_pngs_long.mp4"):
    print("Starting video save")
    # Command to generate video using FFmpeg
    command = [
        "ffmpeg", "-framerate", "15", "-i", f"{output_dir}/frame_%04d.png",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Force even width & height
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        output_video
    ]
    
    subprocess.run(command)

### https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image  ## maybe need, not sure if it works tho
def scale(im, nR, nC):
  nR0 = len(im)     # source number of rows 
  nC0 = len(im[0])  # source number of columns 
  return [[ im[int(nR0 * r / nR)][int(nC0 * c / nC)]  
             for c in range(nC)] for r in range(nR)]

# Creating directories for frames and heatmaps
output_dir_heatmaps = "heatmaps"
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
os.makedirs(output_dir_heatmaps, exist_ok=True)  # Create directory if it doesn't exist

# Dijkstras Directions
DIRECTIONS = [
    (0, 1), (0, -1), (1, 0), (-1, 0),  # Cardinal directions
    (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
]

# Hardcoded colormap selection and alpha set
c_map = mpl.colormaps.get_cmap('jet')
c_map.set_bad(color=(0,0,0,0))

# Hardcoded sensor location data
sensor_positions = {
    'sensor1': (630,925),
    'sensor2': (328, 323),
    'sensor3': (1091, 1597),
    'sensor4': (1880, 2331),
    'sensor5': (719, 886)
}

# Hardcoded sensor names
sensor_names =  ('sensor1','sensor2','sensor3','sensor4','sensor5')

# Hardcoded csv input
df1 = pd.read_csv('sensor1.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df2 = pd.read_csv('sensor2.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df3 = pd.read_csv('sensor3.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df4 = pd.read_csv('sensor4.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df5 = pd.read_csv('sensor5.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
dfs = [df1,df2,df3,df4,df5]

# Hardcoded timestamp input
timestamps = df1['Date-Time'].to_list()

#Creates dictionary for each csv pd array with the datetime as index (ie there is no 0,1,2,3,4,5, etc) ONLY TWO COLUMNS
dcs = []
for df in dfs:
    df = df.set_index('Date-Time')
    dc = df.to_dict('index')
    dcs.append(dc)

#Hard coded cave map upload
cave_map = load_cave_map("Howards_Waterfall_Cave_Map-1.png")

#Resolution of cave map
x_size = cave_map.shape[1]
y_size = cave_map.shape[0]

#set figure size 
n = 100
fig,ax = plt.subplots(figsize=(x_size / n, y_size / n))

# Prepare grid
grid_x, grid_y = np.meshgrid(np.linspace(0, x_size, x_size), np.linspace(0, y_size, y_size))

# Get mask  
mask = get_mask()
mask_list = mask.tolist()

# Extract sensor locations
sensor_x = np.array([sensor_positions[key][0] for key in sensor_positions])
sensor_y = np.array([sensor_positions[key][1] for key in sensor_positions])

# Calculate distances with Dijkstra's 
sensor_distances_astar = {sensor: dijkstras(sensor_positions[sensor], mask) for sensor in sensor_positions}
# Save distances                                                                                                ## still need to code the load from this
np.savez_compressed("sensor_distances_star.npz", sensor_distances_astar)

# Hard Coded Frame Selection
start = 180
end = 18180
skip = 60
timestamps_trim = []
for ts in timestamps[start:end:skip]:
    timestamps_trim.append(ts)

# Hard coded Heatmap Generation 
mode = 1
alpha = 2


# Get from file or calculate new --- need to implement a check for when to use which

heatmaps = get_heatmaps(start,end,skip,sensor_distances_astar, alpha, mode)
#heatmaps = get_heatmaps_file()


# Save as pngs
save_heatmaps_png(heatmaps, sensor_x, sensor_y, cave_map, x_size, y_size, timestamps_trim, output_dir)

# Generate the video
generate_video_from_pngs()
print("Ani save done")


