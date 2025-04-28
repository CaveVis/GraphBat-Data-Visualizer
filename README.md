# GraphBat

Welcome to GraphBat!

GraphBat is an **open-sourced**, **Python based**, data visualization app made for speleologists.

## Overview

GraphBat provides a way to visualize sensor data taken with individual sensors within a cave.

* Sensor data should be in a `[Timestamp : Value]` format.
* Input files must have a `.csv` extension to work with GraphBat.
* Once uploaded to a project, the sensor data can be viewed as:
    * Bar graph
    * Box plot
    * Histogram
    * Line graph
    * Heat map overlaid on a map of a cave (or any image).

## Requirements

* **Python:** Version 3.12 or greater
* **Packages:** The following Python packages are required. We recommend using the `pip` install manager.
    ```bash
    pip install matplotlib
    pip install pandas
    pip install pyqt5
    pip install pyside6
    pip install numpy
    pip install numba
    pip install scipy
    pip install pillow
    ```
* **System Resources (Recommended):**
    * RAM: >4GB available
    * Storage: >8GB free space

## Getting Started

1.  **Download:** Download or clone the GraphBat source code.
2.  **Install Dependencies:** Ensure you have Python 3.12+ and install the required packages using the `pip` commands listed in the [Requirements](#requirements) section.
3.  **Run GraphBat:** Navigate to the downloaded directory in your terminal and run the `main.py` file:
    ```bash
    python main.py
    ```

This will launch the GraphBat application.
