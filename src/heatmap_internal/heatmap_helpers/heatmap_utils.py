import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
import os
import subprocess
import heapq
import math
from matplotlib.widgets import Slider
from numba import njit


def get_mask(path="output_list.txt"):
    mask_array = np.load('heatmap_internal/internal_data/my_array.npy')   
    return mask_array


def load_cave_map(image_path):
    cave_map = Image.open(image_path)
    return np.array(cave_map)


def dist_linear(sensor_pos, mask):  
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


def dijkstras(start, mask):                                   
    #  Directions
    directions = [
    (0, 1), (0, -1), (1, 0), (-1, 0),  # Cardinal directions
    (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
    ]
    cols, rows = mask.shape
    distances = {start: 1e-10}  
    priority_queue = [(1e-10, start)]  
    while priority_queue:
        cost, (x, y) = heapq.heappop(priority_queue)

        for direction in directions:
            nx, ny = x + direction[0], y + direction[1]

            if 0 <= nx < rows and 0 <= ny < cols and mask[ny][nx] == 1:
                new_cost = distances[(x, y)] + (1 if abs(direction[0]) + abs(direction[1]) == 1 else math.sqrt(2))

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


def preprocess_data_from_dataframe(data_df, ts, sensor_names, sensor_distances, mask):
    try:
        temperatures = data_df.loc[ts, sensor_names].values
        temperatures = temperatures.astype(np.float64)
    except Exception as e:
        print(f"Lines 88-89 (heatmap_utils.py) : An error occurred during temperature extraction: {e}")
        return None, None
    try:
        grid_shape = (mask.shape[0], mask.shape[1], len(sensor_names))
        sensor_distances_array = np.full(grid_shape, np.inf, dtype=np.float64)

        for i, name in enumerate(sensor_names):
            for (x, y), dist in sensor_distances[name].items():
                if isinstance(x, int) and isinstance(y, int) and \
                   0 <= y < mask.shape[0] and 0 <= x < mask.shape[1]:
                    if isinstance(dist, (int, float)) and not np.isnan(dist):
                        sensor_distances_array[y, x, i] = float(dist)
                    else:
                        print(f"Warning: Invalid distance '{dist}' for sensor '{name}' at ({x},{y}).")
                else:
                    print(f"Warning: Invalid/out-of-bounds coord ({x},{y}) for sensor '{name}'.")

    except Exception as e:
        print(f"An error occurred building the distance array: {e}")
        return None, None

    return temperatures, sensor_distances_array

def get_heatmaps_file(output_dir_heatmaps):
    heatmaps = []
    for filename in sorted(os.listdir(output_dir_heatmaps)):  # Ensure files are loaded in order
        if filename.endswith(".npz"):
            data = np.load(os.path.join(output_dir_heatmaps, filename))  # Load .npz file
            heatmap = data["arr_0"].astype(np.float32)  # Convert to float32
            heatmaps.append(heatmap)
    return heatmaps
def get_sdev_from_dataframe(data_df):
    sensor_columns = data_df.columns.tolist() 
    try:
        selected_data = data_df[sensor_columns]
        all_values = selected_data.values


        sdev = np.nanstd(all_values)
        mean = np.nanmean(all_values)
        return sdev, mean

    except Exception as e:
        print(f"An error occurred during standard deviation calculation: {e}")
        return np.nan

def save_heatmaps_png(sensor_x, sensor_y, cave_map, x_size, y_size, timestamps, output_dir, c_map, avg, sdev_steps, s_dev, mask_, sensor_distances, alpha, dfs, sensor_names):
    
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    i = 0

    for ts in timestamps:
        print(f"Saving frame {i+1}/{len(timestamps)}")
        frame_filename = os.path.join(output_dir, f"frame_{i:04d}.png")
        if not os.path.exists(frame_filename):
            
            temperatures, sensor_distances_array = preprocess_data_from_dataframe(
                dfs, ts, sensor_names,
                sensor_distances, mask_
            )
            heatmap = idw_interpolation(
                temperatures, sensor_distances_array, mask_, alpha
            )
            vmin = avg - (s_dev*sdev_steps)                                                                                            ## Customize sdev nums away for color here
            vmax = avg + (s_dev*sdev_steps)
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
            label_font_size = base_font_size * 1.4
            sensor_font_size = base_font_size * 0.9
            colorbar_font_size = base_font_size * 1.4

            fig, ax = plt.subplots(figsize=(fig_width, fig_height))  
            ax.imshow(cave_map, extent=[0, x_size, 0, y_size], cmap='Greys')
            im = ax.imshow(heatmap, extent=(0, x_size, 0, y_size), origin='lower', alpha = 0.6 ,  cmap=c_map, vmin=vmin, vmax=vmax)
            cbar = fig.colorbar(im, ax=ax, extend='both')
            cbar.set_label('Temperature (°C)', fontsize = colorbar_font_size)
            cbar.cmap.set_over('magenta')
            cbar.cmap.set_under('blueviolet')
            ax.set_title(f"Cave Temperature at {timestamps[i]}", fontsize=title_font_size)   #### need to fix this
            ax.set_xlabel("X Position", fontsize=label_font_size)
            ax.set_ylabel("Y Position", fontsize=label_font_size)
            j=1
            for x, y in zip(sensor_x, sensor_y):  
                ax.text(x, y, "Sensor: "+str(j), fontsize=sensor_font_size, color="white", ha="center", va="bottom",
                        bbox=dict(facecolor='black', edgecolor='none', alpha=0.5, pad=1))
                j+=1

            ax.scatter(sensor_x, sensor_y, c='green', edgecolors='black', label='Sensors')
            plt.savefig(frame_filename, bbox_inches="tight", pad_inches=0, dpi=200)
            print(f"Saved: {frame_filename}")  # Debug message
            fig.clf()  # Clear figure content
            plt.close('all')  # Free memory by closing the figure
        else:
            print(f"Skipped (exists): {frame_filename}")  # Debug message
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
