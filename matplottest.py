import numpy as np
import pandas as pd
from pandas import Timestamp 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import griddata
import time
from PIL import Image
import os
import subprocess
import ast
import math
c_map = mpl.colormaps.get_cmap('plasma')
c_map.set_bad(color=(0,0,0,0))
import math as m

output_dir_heatmaps = "heatmaps"
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
os.makedirs(output_dir_heatmaps, exist_ok=True)  # Create directory if it doesn't exist

#
#
#
#   This will not work as is, takes some specific hardcoding to work properly, you'll need to calculate the heatmaps and save as .npx files.  
#   message me if you want to make this work on your own or wait till i make it more plug n play
#
#
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
        a = m.pow(x-sx,2)
        b = m.pow(y-sy,2)
        value = m.sqrt(a+b)
        return value
    

def idw_interpolation(sx, sy, dcs, grid_x, ts, mask, alpha=1):
    # Create output arrays, initializing with NaN
    top = np.full_like(grid_x, np.nan, dtype=float)
    bottom = np.full_like(grid_x, np.nan, dtype=float)
    final = np.full_like(grid_x, np.nan, dtype=float)
    print(grid_x.shape[0])
    print(grid_x.shape[1])
    for x in range(grid_x.shape[0]-1):
        for y in range(grid_x.shape[1]-1):
            if mask[x][y] == 1:
                top[x][y],bottom[x][y] = 0,0
                for i in range(len(sx)):
                    eps = 1e-10
                    d = max(get_dist((x, y), (sx[i], sy[i])), eps) ** alpha
                    top[x][y] += dcs[i][ts]['Temperature   (°C)'] / d  #### USING HARDCODED KEY HERE
                    bottom[x][y] += 1/d
    
    return top/bottom
def get_heatmaps_file(num_frames):
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

def calc_heatmaps():
    i = 1
    for ts in timestamps[80:19980:20]:    ########## calc a heatmap for every nth timestamp 
        print("Heatmap -- " + str(i))
        i +=1
        max = 0
        heatmap = idw_interpolation(sensor_x, sensor_y, dcs, grid_x, ts, mask)
        for row in range(heatmap.shape[0]):
            for col in range(heatmap.shape[1]):
                if heatmap[row,col] != np.nan and heatmap[row,col] > max:
                    max = heatmap[row,col]
        heatmaps.append(heatmap)
        print(str(max))
        # close the file
    return heatmaps
def get_s_dev(heatmaps):
    all_values = np.concatenate([hm[~np.isnan(hm)].flatten() for hm in heatmaps])  # Flatten and remove NaNs
    avg = np.mean(all_values)  # Compute mea
    top = 0
    for val in all_values:
        top += math.pow(val - avg,2)
    final = math.sqrt(top/all_values.size)
    return final , avg
def save_heatmaps_png(heatmaps, sensor_x, sensor_y, cave_map, x_size, y_size, timestamps, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
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
        cbar.set_label('Temperature (°C)')
        cbar.cmap.set_over('red')
        cbar.cmap.set_under('cyan')
        ax.set_title(f"Cave Temperature at {timestamps[i]}", fontsize=16)   #### need to fix this
        ax.set_xlabel("X Position", fontsize=14)
        ax.set_ylabel("Y Position", fontsize=14)
        j=0
        for x, y in zip(sensor_x, sensor_y):  
            ax.text(x, y, "Sensor: "+str(j), fontsize=10, color="white", ha="center", va="bottom",
                    bbox=dict(facecolor='black', edgecolor='none', alpha=0.5, pad=1))
            j+=1

        ax.scatter(sensor_x, sensor_y, c='green', edgecolors='black', label='Sensors')

        frame_filename = f"{output_dir}/frame_{i:04d}.png"
        plt.savefig(frame_filename, bbox_inches="tight", pad_inches=0, dpi=100)
        plt.close(fig)  # Free memory by closing the figure
        print(f"Saved {frame_filename}")
        i += 1


### https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image
def scale(im, nR, nC):
  nR0 = len(im)     # source number of rows 
  nC0 = len(im[0])  # source number of columns 
  return [[ im[int(nR0 * r / nR)][int(nC0 * c / nC)]  
             for c in range(nC)] for r in range(nR)]




# Hardcoded sensor location data
sensor_positions = {
    'sensor1': (639,937),
    'sensor2': (328, 323),
    'sensor3': (1091, 1597),
    'sensor4': (1880, 2335),
    'sensor5': (719, 886)
}


df1 = pd.read_csv('sensor1.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df2 = pd.read_csv('sensor2.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df3 = pd.read_csv('sensor3.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df4 = pd.read_csv('sensor4.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
df5 = pd.read_csv('sensor5.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
dfs = [df1,df2,df3,df4,df5]

timestamps = df1['Date-Time'].to_list()

dcs = []
for df in dfs:
    df = df.set_index('Date-Time')
    dc = df.to_dict('index')
    dcs.append(dc)
cave_map = load_cave_map("Howards_Waterfall_Cave_Map-1.png")
x_size = cave_map.shape[1]
y_size = cave_map.shape[0]

fig,ax = plt.subplots(figsize=(x_size / 100, y_size / 100))

print(x_size)
print(y_size)
frames = {}


#mask = get_mask()  # Assume user_mask is received from PaintGrid
#print(type(mask))
#print(mask.size)
#mask = scale(mask, y_size,x_size)

# Prepare grid
grid_x, grid_y = np.meshgrid(np.linspace(0, x_size, x_size), np.linspace(0, y_size, y_size))
mask = get_mask()
# Extract sensor locations
sensor_x = np.array([sensor_positions[key][0] for key in sensor_positions])
sensor_y = np.array([sensor_positions[key][1] for key in sensor_positions])
heatmaps = []
# Perform IDW interpolation
#heatmaps = calc_heatmaps()
print("--- calculated heat maps ---")
#save_heatmaps_npz(heatmaps)
#print("--- saved heat maps ---")
heatmaps = get_heatmaps_file(973)
print("--- Got heatmaps from file ---")
save_heatmaps_png(heatmaps, sensor_x, sensor_y, cave_map, x_size, y_size, timestamps, output_dir)
print("--- saved heat pngs ---")




## Need to add sensor labels
def generate_video_from_pngs(output_dir="frames", output_video="output_movie_pngs_long.mp4"):
    print("Starting video save")
    # Command to generate video using FFmpeg
    command = [
        "ffmpeg", "-framerate", "30", "-i", f"{output_dir}/frame_%04d.png",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Force even width & height
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        output_video
    ]
    
    subprocess.run(command)
generate_video_from_pngs()
print("Ani save done")


