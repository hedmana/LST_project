import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime

def load_data():
    # Open file dialog to select CSV file
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if not file_path:
        print("No file selected.")
        return None, None
    # Read CSV file into pandas DataFrame
    return pd.read_csv(file_path), file_path


def plot_data(df, csv_filename):
    # Convert time column to datetime object
    df['time'] = pd.to_datetime(df['time'])

    # Round temperature values to two decimals
    df['temperature'] = df['temperature'].round(2)

    # Plot temperature against time
    plt.plot(df['time'], df['temperature'], marker='o')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature vs Time')
    plt.grid(True)

    # Limit the number of ticks to 5 on the x-axis
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(5))

    # Format the ticks to show only hour and minute
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Save the plot as an image with the same name as the CSV file
    plot_filename = os.path.join("graphs", os.path.splitext(csv_filename)[0] + ".png")
    plt.savefig(plot_filename)
    plt.show()
def main():
    print("Please navigate to the folder containing the CSV file.")
    df, file_path = load_data()
    if df is not None:
        df = df[(df["temperature"] >= 20) & (df["temperature"] <= 100)]
        plot_data(df, os.path.basename(file_path))

if __name__ == "__main__":
    main()
