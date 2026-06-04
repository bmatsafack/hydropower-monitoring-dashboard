#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri May 8 17:22:08 2026
@author: blondelleatsafack
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mdates

# =========================
# CSV files
# =========================
thingspeak_file = "/Users/blondelleatsafack/Documents/Blondelle_Rwanda/RESEARCH_2026/THESIS/1_From_Research2023/thingspeak_data.csv"
python_file = "/Users/blondelleatsafack/Documents/Blondelle_Rwanda/RESEARCH_2026/THESIS/1_From_Research2023/python_data.csv"

# =========================
# Plot style
# =========================
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 14,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 12
})

# =========================
# Load CSV files
# =========================
df_ts = pd.read_csv(thingspeak_file)
df_py = pd.read_csv(python_file)

# =========================
# Rename fields
# =========================
field_map = {
    "field1": "isa",
    "field2": "isb",
    "field3": "isc",
    "field4": "va",
    "field5": "vb",
    "field6": "vc",
    "field7": "pm",
    "field8": "wm"
}

df_ts = df_ts.rename(columns=field_map)
df_py = df_py.rename(columns=field_map)

signals = ["isa", "isb", "isc", "va", "vb", "vc", "pm", "wm"]

# =========================
# Use same number of rows
# =========================
n = min(len(df_ts), len(df_py))

df_ts = df_ts.iloc[:n].copy()
df_py = df_py.iloc[:n].copy()

# =========================
# Create time axis from ThingSpeak timestamp
# =========================
df_ts["time"] = pd.to_datetime(df_ts["created_at"], errors="coerce", utc=True)
df_ts["time"] = df_ts["time"].dt.tz_localize(None)

x = df_ts["time"]

# =========================
# Convert signals to numeric
# =========================
for signal in signals:
    df_ts[signal] = pd.to_numeric(df_ts[signal], errors="coerce")
    df_py[signal] = pd.to_numeric(df_py[signal], errors="coerce")

# =========================
# Y-axis labels
# =========================
ylabel_map = {
    "isa": "Current A (pu)",
    "isb": "Current B (pu)",
    "isc": "Current C (pu)",
    "va": "Voltage A (pu)",
    "vb": "Voltage B (pu)",
    "vc": "Voltage C (pu)",
    "pm": "Mechanical power (pu)",
    "wm": "Rotor speed (pu)"
}

# =========================
# Plot function
# =========================
def plot_block(signals, title):
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    axes = axes.flatten()

    for i, signal in enumerate(signals):

        # ThingSpeak data: green
        axes[i].plot(
            x,
            df_ts[signal],
            label=f"{signal} ThingSpeak",
            linewidth=2,
            color="blue"
        )

        # Python data: blue
        axes[i].plot(
            x,
            df_py[signal],
            label=f"{signal} Python",
            linestyle="--",
            linewidth=3,
            color="red"
        )

        # Axis labels
        axes[i].set_xlabel("Time", fontsize=16)
        axes[i].set_ylabel(ylabel_map[signal], fontsize=16)

        # Increase x-axis and y-axis tick font size
        axes[i].tick_params(axis="x", labelsize=14, rotation=45)
        axes[i].tick_params(axis="y", labelsize=14)

        # Legend
        axes[i].legend(fontsize=12)

        # Remove grid
        axes[i].grid(False)

        # Y-axis formatting
        axes[i].ticklabel_format(style="plain", axis="y")
        axes[i].yaxis.get_offset_text().set_visible(False)
        axes[i].yaxis.set_major_formatter(FormatStrFormatter("%.8f"))

        # Time formatting
        axes[i].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    # Optional title
    # fig.suptitle(title, fontsize=16)

    plt.tight_layout()
    plt.show()

# =========================
# Generate plots
# =========================
plot_block(["isa", "isb", "isc", "va"], "ThingSpeak and Python Plots")
plot_block(["vb", "vc", "pm", "wm"], "ThingSpeak and Python Plots")

print("Plots completed.")