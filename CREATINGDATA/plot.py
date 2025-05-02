from collections import deque
import heapq
from rawdata import communes
import math
import random
import numpy as np
import matplotlib.pyplot as plt

x_coords = []
y_coords = []
commune_names = []
commune_last_words = []
neighbor_coords = {}
skipped = []

for commune, details in communes.items():
    # Check if 'coordinates' are present and have at least 2 elements
    if "coordinates" in details and len(details["coordinates"]) >= 2:
        x_coords.append(details["coordinates"][1])
        y_coords.append(details["coordinates"][0])
        commune_names.append(commune)
        commune_last_words.append(commune.split()[-1])
    else:
        print(f"Skipping commune '{commune}' as it does not have complete coordinates.")
        skipped.append(commune)

    neighbor_coords[commune] = []
    if "neighbors" in details:
        for neighbor in details["neighbors"]:
            if neighbor in communes and "coordinates" in communes[neighbor] and len(communes[neighbor]["coordinates"]) >= 2:
                neighbor_coords[commune].append(communes[neighbor]["coordinates"])

print(len(skipped))

# Calculate appropriate x and y limits
x_min = min(x_coords) - 0.0000001
x_max = max(x_coords) + 0.0000001
y_min = min(y_coords) - 0.00005
y_max = max(y_coords) + 0.00005

# Plot the coordinates
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlabel("Latitude")
ax.set_ylabel("Longitude")
ax.set_title("Communes Coordinates")
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Plot the commune coordinates
scatter = ax.scatter(x_coords, y_coords, color='none', s=20, facecolors='none', edgecolors='none', linewidths=0.4, zorder=2)

# Add the last word of each commune below its node
for i, (x, y) in enumerate(zip(x_coords, y_coords)):
    ax.annotate(commune_last_words[i], (x, y), xytext=(0, -10), textcoords="offset points", ha='center', va='top')

# Draw lines between communes and their neighbors
for commune, coords in neighbor_coords.items():
    try:
        commune_index = commune_names.index(commune)
        commune_x = x_coords[commune_index]
        commune_y = y_coords[commune_index]
        for neighbor_coord in coords:
            # Get the name of the neighbor commune
            neighbor_name = [name for name, details in communes.items() if details["coordinates"] == neighbor_coord][0]
            # Check if the current commune is also a neighbor of the neighbor commune
            if commune in communes[neighbor_name]["neighbors"]:
                neighbor_x = neighbor_coord[1]
                neighbor_y = neighbor_coord[0]
                ax.plot([commune_x, neighbor_x], [commune_y, neighbor_y], '#CC6975', linewidth=2, zorder=1)
    except ValueError as e:
        print(f"Error processing commune '{commune}': {e}")

# Save the plot without a background
plt.savefig('plot_without_background.png', bbox_inches='tight', transparent=True)

num_nodes = len(communes)
print(f"Number of nodes: {num_nodes}")

plt.show()