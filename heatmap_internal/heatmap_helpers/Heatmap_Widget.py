import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PIL import Image
from matplotlib.widgets import Slider as MplSlider 
from numba import njit
from heatmap_internal.heatmap_helpers.MplCanvas import * 
from heatmap_internal.heatmap_helpers.heatmap_utils import *

class HeatmapViewerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        self.canvas = MplCanvas(self, width=12, height=8, dpi=100) # CANVAS SIZING 
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # --- Store plotting elements and data ---
        self.im = None 
        self.title = None 
        self.timestamp_text = None 
        self.cbar = None # colorbar
        self.slider = None # Matplotlib Slider
        self.slider_ax = None # Axes for the slider
        self.timestamp_ax = None 

        # Data attributes (populated by plot_data)
        self.dfs = None
        self.timestamps = None
        self.sensor_x = None
        self.sensor_y = None
        self.cave_map = None
        self.x_size = None
        self.y_size = None
        self.c_map = None
        self.mask_ = None
        self.sensor_distances = None
        self.sensor_names = None
        self.s_dev = None
        self.avg = None
        self.sdev_steps = None
        self.alpha = None

    def plot_data(self, dfs, timestamps, sensor_x, sensor_y, cave_map, mask_,
                    sensor_distances, sensor_names, s_dev, avg, sdev_steps=2,
                    alpha=1, c_map_name='jet'):
        # Store data
        self.dfs = dfs
        self.timestamps = timestamps
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y
        self.cave_map = cave_map
        self.x_size = cave_map.shape[1]
        self.y_size = cave_map.shape[0]
        self.c_map = mpl.colormaps.get_cmap(c_map_name)
        self.c_map.set_bad(color=(0,0,0,0)) # NaN transparency
        self.mask_ = mask_
        self.sensor_distances = sensor_distances
        self.sensor_names = sensor_names
        self.s_dev = s_dev
        self.avg = avg
        self.sdev_steps = sdev_steps
        self.alpha = alpha

        # --- Clear previous plot elements if any ---
        self.canvas.clear_axes()
        if self.cbar:
            try:
                self.cbar.remove()
            except Exception: 
                pass
            self.cbar = None
        if self.slider_ax:
            try:
                self.canvas.fig.delaxes(self.slider_ax)
            except Exception:
                pass
            self.slider_ax = None
            self.slider = None # Slider needs recreation if axes change
        if self.timestamp_ax:
             try:
                self.canvas.fig.delaxes(self.timestamp_ax)
             except Exception:
                pass
             self.timestamp_ax = None
             self.timestamp_text = None

        i = 0

        temperatures, sensor_distances_array = preprocess_data_from_dataframe(
            self.dfs, self.timestamps[i], self.sensor_names,
            self.sensor_distances, self.mask_
        )
        initial_heatmap = idw_interpolation(
            temperatures, sensor_distances_array, self.mask_, self.alpha
        )

       
        ax = self.canvas.axes 
        fig = self.canvas.fig 

        vmin = self.avg - (self.s_dev * self.sdev_steps)
        vmax = self.avg + (self.s_dev * self.sdev_steps)


        base_font_size = 10 

        title_font_size = base_font_size * 1.2
        label_font_size = base_font_size
        sensor_font_size = base_font_size * 0.8
        colorbar_font_size = base_font_size

        # Plot cave map background
        ax.imshow(self.cave_map, extent=[0, self.x_size, 0, self.y_size], cmap='Greys')

        # Plot heatmap
        self.im = ax.imshow(
            initial_heatmap, extent=(0, self.x_size, 0, self.y_size), origin='lower',
            alpha=0.6, cmap=self.c_map, vmin=vmin, vmax=vmax
        )

        # Colorbar
        self.cbar = fig.colorbar(self.im, ax=ax, extend='both')
        self.cbar.set_label('Temperature (°C)', fontsize=colorbar_font_size)
        self.cbar.cmap.set_over('magenta')
        self.cbar.cmap.set_under('blueviolet')
        self._set_cbar_extend_colors() # Helper to set colors correctly

        # Title and Labels
        self.title = ax.set_title(
            f"Cave Temperature at {self.timestamps[i]}", fontsize=title_font_size
        )
        ax.set_xlabel("X Position", fontsize=label_font_size)
        ax.set_ylabel("Y Position", fontsize=label_font_size)

        # Plot Sensors
        j=1
        for x, y in zip(self.sensor_x, self.sensor_y):
            ax.text(x, y, f"S{j}", fontsize=sensor_font_size, color="white", ha="center", va="bottom",
                    bbox=dict(facecolor='black', edgecolor='none', alpha=0.5, pad=0.5))
            j+=1
        ax.scatter(self.sensor_x, self.sensor_y, s=20, c='lime', edgecolors='black', label='Sensors')

        # --- Add Slider and Timestamp Text using fig.add_axes ---
        # Adjust layout to make space
        fig.subplots_adjust(bottom=0.2) # Increase bottom margin

        # Timestamp text above slider
        self.timestamp_ax = fig.add_axes([0.2, 0.1, 0.6, 0.03]) # Position relative to figure
        self.timestamp_text = self.timestamp_ax.text(
            0.5, 0.5, f"{self.timestamps[i]}", fontsize=label_font_size,
            ha='center', va='center', transform=self.timestamp_ax.transAxes
        )
        self.timestamp_ax.set_xticks([])
        self.timestamp_ax.set_yticks([])
        self.timestamp_ax.set_frame_on(False)

        # Matplotlib Slider
        self.slider_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03]) # Position relative to figure
        self.slider = MplSlider(
            self.slider_ax, 'Time', 0, len(self.timestamps)-1,
            valinit=0, valstep=1
        )

        # Connect slider update function
        self.slider.on_changed(self._update_plot)

        # Initial draw
        self.canvas.redraw()

    def _set_cbar_extend_colors(self):
        """Sets the over/under colors on the colorbar correctly."""
        if self.cbar:
            # Sometimes requires accessing internal patches
             try:
                  if self.cbar.extend in ('both', 'max'):
                       self.cbar.ax.patches[-1].set_facecolor('magenta') # Top arrow
                  if self.cbar.extend in ('both', 'min'):
                       self.cbar.ax.patches[0].set_facecolor('blueviolet') # Bottom arrow
             except Exception as e:
                  print(f"Warning: Could not set colorbar extend colors: {e}")


    def _update_plot(self, val):
        """Internal function called when the slider value changes."""
        if self.im is None or self.timestamps is None: # Not initialized
            return

        i = int(self.slider.val) # Get integer index from slider

        # Recalculate heatmap for the selected timestamp
        try:
            temperatures, sensor_distances_array = preprocess_data_from_dataframe(
                self.dfs, self.timestamps[i], self.sensor_names,
                self.sensor_distances, self.mask_
            )
            new_heatmap = idw_interpolation(
                temperatures, sensor_distances_array, self.mask_, self.alpha
            )
        except Exception as e:
            print(f"Error calculating heatmap for timestamp {self.timestamps[i]}: {e}")
            # Optionally display error on plot or skip update
            return

        # Update plot elements
        self.im.set_data(new_heatmap)
        self.title.set_text(f"Cave Temperature at {self.timestamps[i]}")
        self.timestamp_text.set_text(f"{self.timestamps[i]}")

        # Ensure colorbar extend colors are persistent
        self._set_cbar_extend_colors()

        # Redraw the canvas
        self.canvas.redraw()

    def generate_movie(self):                 
        save_heatmaps_png(self.sensor_x, self.sensor_y, self.cave_map, self.x_size, self.y_size, self.timestamps, "frames", self.c_map, self.avg, self.sdev_steps, self.s_dev,  self.mask_, self.sensor_distances, self.alpha, self.dfs, self.sensor_names)
        fps = 30                             ## SET FPS 
        generate_video_from_pngs(fps)