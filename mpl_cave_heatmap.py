import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
import os
import subprocess
import heapq
import math
#import objgraph                         ## Testing stuff
#import tracemalloc 
import gc
import time
#import line_profiler
from matplotlib.widgets import Slider
from numba import njit




t0 = time.time()

#print("           __ OBJGRAPH __")
#objgraph.show_growth()
#print("         __ OBJGRAPH END __")
#tracemalloc.start()
#snapshot1 = tracemalloc.take_snapshot()

#@line_profiler.profile
def get_mask(path="output_list.txt"):
    mask_array = np.load('my_array.npy')
    return mask_array

#@line_profiler.profile
def load_cave_map(image_path):
    cave_map = Image.open(image_path)
    return np.array(cave_map)

#@line_profiler.profile
def dist_linear(sensor_pos, mask):  ## straight line            need to redo this to work with @njit
    sx = sensor_pos[0]
    sy = sensor_pos[1]
    x_size = mask.shape[1]
    y_size = mask.shape[0]
    distances = {sensor_pos: 1e-10}
    for x in range(x_size):
        for y in range(y_size):
            if mask[y][x] == 1:
                if x == sx and y == sy:
                    continue
                else:
                    a = math.pow(x-sx,2)
                    b = math.pow(y-sy,2)
                    value = math.sqrt(a+b)
                    distances[(x,y)]=value
    return distances

#@line_profiler.profile
def dijkstras(start, mask):                                    # need to redo this to work with @njit
    # Dijkstras Directions
    directions = [
    (0, 1), (0, -1), (1, 0), (-1, 0),  # Cardinal directions
    (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
    ]
    cols, rows = mask.shape
    distances = {start: 1e-10}  # Stores shortest distance to each point
    priority_queue = [(1e-10, start)]  # (cost, (x, y))
    while priority_queue:
        cost, (x, y) = heapq.heappop(priority_queue)
        #print("ENTERED WHILE LOOP")

        ##
        ## EDGE CASE ERRORS HERE ?? 
        ##
        

        for direction in directions:
            nx, ny = x + direction[0], y + direction[1]

            if 0 <= nx < rows and 0 <= ny < cols and mask[ny][nx] == 1:
                new_cost = distances[(x, y)] + (1 if abs(direction[0]) + abs(direction[1]) == 1 else math.sqrt(2))
                # Update if this path is better
                if new_cost < distances.get((nx, ny), float('inf')):
                    distances[(nx, ny)] = new_cost
                    heapq.heappush(priority_queue, (new_cost, (nx, ny)))
    return distances

@njit
def calculate_idw_point(temperatures, distances, alpha):
    weights = 1.0 / (distances ** alpha)
    weighted_temp = np.dot(weights, temperatures)
    sum_weights = np.sum(weights)
    return weighted_temp / sum_weights if sum_weights != 0 else np.nan

@njit
def idw_interpolation(temperatures, sensor_distances, mask, alpha):
    valid_indices = np.argwhere(mask == 1)
    result = np.full_like(mask, np.nan, dtype=np.float64)

    for pos in valid_indices:
        idx = pos[0], pos[1]
        distances = sensor_distances[idx]  # Extract distances for this grid point
        result[idx] = calculate_idw_point(temperatures, distances, alpha)
    
    return result

# Preprocessing: Convert dictionaries to NumPy arrays
def preprocess_data(sx, dcs, ts, sensor_names, sensor_distances, mask):
    # Extract temperature values as a NumPy array
    temperatures = np.array([dcs[i][ts]['Temperature   (°C)'] for i in range(len(sx))], dtype=np.float64)
    
    # Convert sensor distances into a NumPy array for fast lookup
    grid_shape = (mask.shape[0], mask.shape[1], len(sensor_names))
    sensor_distances_array = np.full(grid_shape, np.inf, dtype=np.float64)

    for i, name in enumerate(sensor_names):
        for (x, y), dist in sensor_distances[name].items():
            sensor_distances_array[y, x, i] = dist

    return temperatures, sensor_distances_array

#@line_profiler.profile
def get_heatmaps_file(output_dir_heatmaps):
    heatmaps = []
    for filename in sorted(os.listdir(output_dir_heatmaps)):  # Ensure files are loaded in order
        if filename.endswith(".npz"):
            data = np.load(os.path.join(output_dir_heatmaps, filename))  # Load .npz file
            heatmap = data["arr_0"].astype(np.float32)  # Convert to float32
            heatmaps.append(heatmap)
    return heatmaps


def save_heatmaps_npz(heatmaps, output_dir_heatmaps):
    """Saves a list of NumPy arrays to a .npz file."""
    os.makedirs(output_dir_heatmaps, exist_ok=True)  # Ensure directory exists

    for i, heatmap in enumerate(heatmaps):
        np.savez_compressed(f"{output_dir_heatmaps}/heatmap_{i:04d}.npz", heatmap)  # Save each frame

# Bulk heatmap gen (not used currently)
#@line_profiler.profile         
def get_heatmaps(timestamps_trim, sensor_x, dcs, mask, sensor_distances_linear, sensor_distances_dijkstras, sensor_names, alpha = 1, mode = 0):
    i = 1
    sensor_distances = sensor_distances_linear if mode == 0 else sensor_distances_dijkstras
    heatmaps = []
    for ts in timestamps_trim:    ########## calc a heatmap for every nth timestamp 
        temperatures, sensor_distances_array = preprocess_data(sensor_x, dcs, ts, sensor_names, sensor_distances, mask)
        print("Heatmap -- " + str(i))
        i +=1
        heatmap = idw_interpolation(temperatures, sensor_distances_array, mask, alpha)
        heatmaps.append(heatmap)
        
    #save_heatmaps_npz(heatmaps, output_dir_heatmaps)       ## dont do this since it takes so much space and we got the speed to a more acceptable level
    return heatmaps
@njit
def calculate_sdev(values):
    total = 0.0
    count = 0
    # Compute mean
    for val in values:
        total += val
        count += 1
    if count == 0:
        return 0.0, 0.0  # Avoid division by zero
    mean = total / count

    # Compute variance
    variance_sum = 0.0
    for val in values:
        variance_sum += (val - mean) ** 2
    std_dev = np.sqrt(variance_sum / count)

    return std_dev, mean

def get_sdev_from_dfs(dfs, temp_column='Temperature   (°C)'):
    #Extracts temperature data from multiple DataFrames and computes std dev using Numba
    all_values = np.concatenate([df[temp_column].dropna().values for df in dfs])  # Remove NaNs and merge
    return calculate_sdev(all_values)
#bulk s_dev
def get_s_dev(heatmaps):
    #Compute standard deviation and mean from all valid (non-NaN) heatmap values
    all_values = heatmaps[~np.isnan(heatmaps)]  # Remove NaNs directly using NumPy mask
    avg = np.mean(all_values)  # Compute mean
    variance = np.sum(np.square(all_values - avg)) / all_values.size  # Compute variance
    std_dev = np.sqrt(variance)  # Standard deviation
    return std_dev, avg
#single s_dev
def get_s_dev1(heatmap):
    all_values = heatmap[~np.isnan(heatmap)].flatten()   # Flatten and remove NaNs
    avg = np.mean(all_values)  # Compute mea
    top = 0
    for val in all_values:
        top += math.pow(val - avg,2)
    final = math.sqrt(top/all_values.size)
    return final , avg

def save_heatmaps_png(sensor_x, sensor_y, cave_map, x_size, y_size, timestamps, output_dir, c_map, avg, s_dev, mask, sensor_distances, alpha, dcs, sensor_names):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    vmin = avg - (s_dev*2)                                                                                            ## Customize sdev nums away for color here
    vmax = avg + (s_dev*2)
    i = 0

    for ts in timestamps:
        print(f"Saving frame {i+1}/{len(timestamps)}")
        temperatures, sensor_distances_array = preprocess_data(sensor_x, dcs, ts, sensor_names, sensor_distances, mask)
        heatmap = idw_interpolation(temperatures, sensor_distances_array, mask, alpha)
      
        fig,ax = plt.subplots(figsize=(x_size / 100, y_size / 100))                                         ### Window sizing here

        ax.imshow(cave_map, extent=[0, x_size, 0, y_size], cmap='Greys')
        im = ax.imshow(heatmap, extent=(0, x_size, 0, y_size), origin='lower', alpha = 0.5 ,  cmap=c_map, vmin=vmin, vmax=vmax)
        cbar = fig.colorbar(im, ax=ax, extend='both')
        cbar.set_label('Temperature (°C)', fontsize = 20)
        cbar.cmap.set_over('magenta')
        cbar.cmap.set_under('blueviolet')
        ax.set_title(f"Cave Temperature at {timestamps[i]}", fontsize=25)   #### need to fix this
        ax.set_xlabel("X Position", fontsize=20)
        ax.set_ylabel("Y Position", fontsize=20)
        j=1
        for x, y in zip(sensor_x, sensor_y):  
            ax.text(x, y, "Sensor: "+str(j), fontsize=15, color="white", ha="center", va="bottom",
                    bbox=dict(facecolor='black', edgecolor='none', alpha=0.5, pad=1))
            j+=1

        ax.scatter(sensor_x, sensor_y, c='green', edgecolors='black', label='Sensors')             # Customize color here 

        frame_filename = os.path.join(output_dir, f"frame_{i:04d}.png")
        if not os.path.exists(frame_filename):
            plt.savefig(frame_filename, bbox_inches="tight", pad_inches=0, dpi=100)
            print(f"Saved: {frame_filename}")  # Debug message
        else:
            print(f"Skipped (exists): {frame_filename}")  # Debug message

                       
        fig.clf()  # Clear figure content
        plt.close('all')  # Free memory by closing the figure
        i += 1

def generate_video_from_pngs(fps,output_dir="frames", output_video="output_movie_pngs_long.mp4"):
    print("Starting video save")
    # Command to generate video using FFmpeg
    command = [                                                                                     #### customizable stuff here
        "ffmpeg", "-framerate", f"{fps}", "-i", f"{output_dir}/frame_%04d.png",                         #
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Force even width & height                    #  
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",                  #
        output_video
    ]
    
    subprocess.run(command)

### https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image  ## maybe need, not sure if it works tho
def scale(im, nR, nC):
  nR0 = len(im)     # source number of rows 
  nC0 = len(im[0])  # source number of columns 
  return [[ im[int(nR0 * r / nR)][int(nC0 * c / nC)]  
             for c in range(nC)] for r in range(nR)]


def interactive_viewer(dcs, timestamps, sensor_x, sensor_y, cave_map, x_size, y_size, c_map, mask, sensor_distances, sensor_names, s_dev, avg, alpha=1): 
    #def interactive_viewer(heatmaps, timestamps, sensor_x, sensor_y, cave_map, x_size, y_size, c_map, output_dir_frames):    ## Need to make sure EVERYTHING in here uses same settings as save_as_pngs 
    temperatures, sensor_distances_array = preprocess_data(sensor_x, dcs, timestamps[0], sensor_names, sensor_distances, mask)
    heatmap = idw_interpolation(temperatures, sensor_distances_array, mask, alpha)
    #s_dev = get_s_dev(heatmaps)
    vmin = avg - (s_dev*2)                                                                                            ## Customize sdev nums away for color here
    vmax = avg + (s_dev*2)
        # Limit max figure size 
    max_width, max_height = 12, 8  # Set height in inches
    aspect_ratio = x_size / y_size

    if aspect_ratio > 1:
        fig_width = max_width
        fig_height = max_width / aspect_ratio
    else:
        fig_height = max_height
        fig_width = max_height * aspect_ratio

    base_font_size = max(fig_width * 1.2, 10)  # Scale font but keep a minimum size of 10
    title_font_size = base_font_size * 1.5
    label_font_size = base_font_size * 1.2
    sensor_font_size = base_font_size * 0.8
    colorbar_font_size = base_font_size * 1.1

    i = 0
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))                                  
    ax.imshow(cave_map, extent=[0, x_size, 0, y_size], cmap='Greys')
    im = ax.imshow(heatmap, extent=(0, x_size, 0, y_size), origin='lower', alpha = .5 ,  cmap=c_map, vmin=vmin, vmax=vmax)
    cbar = fig.colorbar(im, ax=ax, extend='both')
    cbar.set_label('Temperature (°C)', fontsize = colorbar_font_size)
    cbar.cmap.set_over('magenta')
    cbar.cmap.set_under('blueviolet')
    cbar.ax.patches[-1].set_facecolor('magenta') 
    cbar.ax.patches[0].set_facecolor('blueviolet')
    title = ax.set_title(f"Cave Temperature at {timestamps[i]}", fontsize=title_font_size) 
    ax.set_xlabel("X Position", fontsize=label_font_size)
    ax.set_ylabel("Y Position", fontsize=label_font_size)
    j=1
    for x, y in zip(sensor_x, sensor_y):  
        ax.text(x, y, "Sensor: "+str(j), fontsize=sensor_font_size, color="white", ha="center", va="bottom",
                bbox=dict(facecolor='black', edgecolor='none', alpha=0.5, pad=1))
        j+=1
    ax.scatter(sensor_x, sensor_y, c='green', edgecolors='black', label='Sensors') 

    plt.subplots_adjust(bottom=0.15)  # Space for slider

    # Timestamp text above slider
    ax_timestamp = plt.axes([0.2, 0.1, 0.6, 0.03])  
    timestamp_text = ax_timestamp.text(0.5, 0.5, f"{timestamps[i]}", fontsize=label_font_size,
                                       ha='center', va='center', transform=ax_timestamp.transAxes)
    ax_timestamp.set_xticks([])
    ax_timestamp.set_yticks([])
    ax_timestamp.set_frame_on(False)


    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # Position of slider
    slider = Slider(ax_slider, 'Time', 0, len(timestamps)-1, valinit=0, valstep=1)
    # Update function

    def update(val):
        i = int(slider.val)
        temperatures, sensor_distances_array = preprocess_data(sensor_x, dcs, timestamps[i], sensor_names, sensor_distances, mask)
        n_heatmap = idw_interpolation(temperatures,sensor_distances_array, mask, alpha) 
        im.set_data(n_heatmap)  # Update heatmap
        title.set_text(f"Cave Temperature at {timestamps[i]}")  # Update title
        timestamp_text.set_text(f"{timestamps[i]}")
        cbar.ax.patches[-1].set_facecolor('magenta')  # Top arrow
        cbar.ax.patches[0].set_facecolor('blueviolet')
        fig.canvas.draw_idle()  # Redraw

    slider.on_changed(update)  # Connect slider to update function

    plt.show()

def main():
   # Creating directories for frames and heatmaps
    output_dir_frames = "frames"
    output_dir_heatmaps = "heatmaps"

    os.makedirs(output_dir_frames, exist_ok=True)    # Create directory if it doesn't exist 
    os.makedirs(output_dir_heatmaps, exist_ok=True)  # Create directory if it doesn't exist

    # Hardcoded colormap selection and alpha set
    c_map = mpl.colormaps.get_cmap('jet')
    c_map.set_bad(color=(0,0,0,0))

    # Hardcoded sensor location data                 # Tbh idk how to allow a drag and drop, manual entering will be fine for now, but kinda sucks for sure.  
    sensor_positions = {                             # Maybe we can do a like select a sensor and then click where you want it to go?  we can grab click position probably and use that
        'sensor1': (630,925),                                  
        'sensor2': (328, 323),
        'sensor3': (1091, 1597),
        'sensor4': (1880, 2331),
        'sensor5': (719, 886)
    }

    # Hardcoded sensor names                                                 ## Need to grab these from files somehow
    sensor_names =  ('sensor1','sensor2','sensor3','sensor4','sensor5')

    tcsv0 = time.time()
    # Hardcoded csv input                                                                       # Get dictionaries from pd  
    df1 = pd.read_csv('sensor1.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')          
    df2 = pd.read_csv('sensor2.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
    df3 = pd.read_csv('sensor3.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
    df4 = pd.read_csv('sensor4.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
    df5 = pd.read_csv('sensor5.csv', index_col=0, parse_dates=[1],on_bad_lines='skip')
    dfs = [df1,df2,df3,df4,df5]
    tcsv1 = time.time()
    print("Time to import csv:{:.4} s".format(tcsv1-tcsv0))



    # Hardcoded timestamp input                                                                # grabs timestamps - need a way to do this dynamically w timestamp column name
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

    # Hard Coded Frame Selection
    start = 240
    end = 19240
    skip = 190
    if(len(timestamps)<end):
        end = len(timestamps)
    timestamps_trim = []
    for ts in timestamps[start:end:skip]:
        timestamps_trim.append(ts)

    # Get mask  
    mask = get_mask()

    # Extract sensor locations
    sensor_x = np.array([sensor_positions[key][0] for key in sensor_positions])
    sensor_y = np.array([sensor_positions[key][1] for key in sensor_positions])

    # Calculate distances with Dijkstra's 

    # need functions to load these from files, but that brings more questions (overwrite the saved one right when they change something? idk) 
    tplindin0 = time.time()
    #sensor_distances_linear = {sensor: dist_linear(sensor_positions[sensor], mask) for sensor in sensor_positions}
    #np.savez_compressed("sensor_distances_lin.npz", **sensor_distances_linear) 

    sensor_distances_linear = dict(np.load("sensor_distances_lin.npz", allow_pickle=True))
    sensor_distances_linear = {key: sensor_distances_linear[key].item() for key in sensor_distances_linear}
    tplindin1 = time.time()
    print("Time to get and save linear distances: {:.4} s".format(tplindin1-tplindin0))

    tpf0 = time.time()
    
    #sensor_distances_dijkstras = {sensor: dijkstras(sensor_positions[sensor], mask) for sensor in sensor_positions}
    #np.savez_compressed("sensor_distances_djk.npz", **sensor_distances_dijkstras)

    sensor_distances_dijkstras = dict(np.load("sensor_distances_djk.npz", allow_pickle=True))     
    sensor_distances_dijkstras = {key: sensor_distances_dijkstras[key].item() for key in sensor_distances_dijkstras}   
    #print(sensor_distances_dijkstras.keys())                                                                        

    tpf1 = time.time()
    print("Time to get and save Dijkstras distances: {:.4} s".format(tpf1-tpf0))
    gc.collect()


    # Hard coded Heatmap Generation 
    mode = 1
    alpha = 2  ## higher alpha makes the dropoff more steep, too low (ie 1) can cause a 'wrap around' effect that is not very good
    #sdev_steps = 2 
    sensor_distances = sensor_distances_linear if mode == 0 else sensor_distances_dijkstras

    tsd0 = time.time()
    std_dev, mean = get_sdev_from_dfs(dfs)
    tsd1 = time.time()
    print(f"Time to get sdev: {tsd1-tsd0:.4}s ")
    print(f"Standard Deviation: {std_dev}, Mean: {mean}")
    gc.collect()
    
                     
    print("Starting Viewer")
    interactive_viewer(dcs, timestamps_trim, sensor_x, sensor_y, cave_map, x_size, y_size, c_map, mask, sensor_distances, sensor_names, std_dev, mean, alpha)
    #interactive_viewer(heatmaps, timestamps_trim, sensor_x, sensor_y, cave_map, x_size, y_size, c_map, output_dir_frames)
    print("Continuing")

    # Save as pngs
    # this also takes quite a while for many timestamps
    tpng0 = time.time()
                      
    save_heatmaps_png(sensor_x, sensor_y, cave_map, x_size, y_size, timestamps_trim, output_dir_frames, c_map, mean, std_dev,  mask, sensor_distances, alpha, dcs, sensor_names)
    tpng1 = time.time()
    print(f"Time to save {(end-start)/skip} pngs: {tpng1-tpng0:.4} s")
    gc.collect()

    # Generate the video
    tvid0 = time.time()
    fps = 10                                ## SET FPS 
    generate_video_from_pngs(fps)
    tvid1 = time.time()
    print("Time to save video {:.4}".format(tvid1-tvid0))
    print("Ani save done")

    gc.collect()

    #snapshot2 = tracemalloc.take_snapshot()
    #print("         __ Tracemalloc __")
    #stats = snapshot2.compare_to(snapshot1, 'lineno')
    #for stat in stats[:10]:
    #    print(stat)
    #print("       __ Tracemalloc END __")

    #print("         __ OBJGRAPH __")
    #objgraph.show_growth()
    #print("       __ OBJGRAPH END __")

    t1 = time.time()
    print("Total completion time {:.4} s".format(t1-t0)) 

if __name__ == "__main__":
    main()
