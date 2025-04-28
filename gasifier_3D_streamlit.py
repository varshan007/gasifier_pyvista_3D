import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.title("3D Exploded Model of Throat-Type Downdraft Gasifier")

# Sidebar for user inputs
st.sidebar.header("Gasifier Geometry Inputs")
gasifier_height = st.sidebar.number_input("Gasifier Height (m)", 1.0, 3.0, 1.2)
gasifier_diameter = st.sidebar.number_input("Gasifier Diameter (m)", 0.2, 1.0, 0.4)
throat_diameter = st.sidebar.number_input("Throat Diameter (m)", 0.05, 0.5, 0.1)
throat_height = st.sidebar.number_input("Throat Height (m)", 0.02, 0.2, 0.06)
throat_ratio = st.sidebar.number_input("Throat Ratio", 0.1, 0.9, 0.25)
steam_inlet_height = st.sidebar.number_input("Steam Inlet Distance Above Throat (m)", 0.05, 0.5, 0.2)
air_inlet_height = st.sidebar.number_input("Air Inlet Distance Above Throat (m)", 0.05, 0.5, 0.1)
air_inlet_diameter = st.sidebar.number_input("Air Inlet Diameter (m)", 0.01, 0.1, 0.016)
steam_inlet_diameter = st.sidebar.number_input("Steam Inlet Diameter (m)", 0.01, 0.1, 0.016)
coal_diameter = st.sidebar.number_input("Coal Diameter (m)", 0.01, 0.1, 0.03)
drying_length = st.sidebar.number_input("Drying Zone Length (m)", 0.05, 0.5, 0.2)
pyrolysis_length = st.sidebar.number_input("Pyrolysis Zone Length (m)", 0.05, 0.5, 0.25)
combustion_length = st.sidebar.number_input("Combustion Zone Length (m)", 0.05, 0.5, 0.25)
reduction_length = st.sidebar.number_input("Reduction Zone Length (m)", 0.05, 0.5, 0.2)
grate_diameter = st.sidebar.number_input("Grate Diameter (m)", 0.05, 0.5, 0.18)
syngas_outlet_diameter = st.sidebar.number_input("Syngas Outlet Diameter (m)", 0.01, 0.1, 0.04)

zone_lengths = [drying_length, pyrolysis_length, combustion_length, reduction_length]

# Helper functions (same as previous script)
def plot_cylinder(ax, radius, height, z_offset, color='gray', alpha=0.7):
    theta = np.linspace(0, 2*np.pi, 60)
    z = np.linspace(0, height, 2)
    theta, z = np.meshgrid(theta, z)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = z + z_offset
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0)

def plot_cone(ax, r_base, r_top, height, z_offset, color='orange', alpha=0.7):
    theta = np.linspace(0, 2 * np.pi, 60)
    z = np.linspace(0, height, 2)
    theta, z = np.meshgrid(theta, z)
    r = r_base + (r_top - r_base) * (z / height)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = z + z_offset
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0)

def plot_inlet(ax, diameter, length, center, z_offset, orientation='radial', color='blue', alpha=0.8):
    r = diameter / 2
    theta = np.linspace(0, 2*np.pi, 30)
    z = np.linspace(0, length, 2)
    theta, z = np.meshgrid(theta, z)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = z + z_offset
    if orientation == 'radial':
        x, z = z, x
        y, z = y, z
    x, y, z = x + center[0], y + center[1], z
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0)

# Plotting
fig = plt.figure(figsize=(8, 10))
ax = fig.add_subplot(111, projection='3d')

explode_offsets = [0, 0.25, 0.55, 0.85, 1.1]
zone_colors = ['tan', 'sandybrown', 'red', 'green']
z_base = 0
for i, (length, color) in enumerate(zip(zone_lengths, zone_colors)):
    plot_cylinder(ax, gasifier_diameter/2, length, explode_offsets[i], color=color, alpha=0.8)
    z_base += length

plot_cone(ax, gasifier_diameter/2, throat_diameter/2, throat_height, explode_offsets[3]+zone_lengths[-1], color='orange', alpha=0.9)
plot_cylinder(ax, grate_diameter/2, 0.02, explode_offsets[4]+throat_height, color='gray', alpha=0.7)
plot_cylinder(ax, syngas_outlet_diameter/2, 0.15, explode_offsets[4]+throat_height+0.02, color='blue', alpha=0.8)

for angle in [0, np.pi]:
    x = (gasifier_diameter/2) * np.cos(angle)
    y = (gasifier_diameter/2) * np.sin(angle)
    plot_inlet(ax, air_inlet_diameter, 0.1, (x, y), explode_offsets[2]+zone_lengths[2]-air_inlet_height, orientation='radial', color='cyan')

for angle in [np.pi/2, 3*np.pi/2]:
    x = (gasifier_diameter/2) * np.cos(angle)
    y = (gasifier_diameter/2) * np.sin(angle)
    plot_inlet(ax, steam_inlet_diameter, 0.1, (x, y), explode_offsets[2]+zone_lengths[2]-steam_inlet_height, orientation='radial', color='magenta')

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('Exploded 3D Model of Throat-Type Downdraft Gasifier')
ax.set_box_aspect([1,1,2])
st.pyplot(fig)  # Display in Streamlit[5][4]