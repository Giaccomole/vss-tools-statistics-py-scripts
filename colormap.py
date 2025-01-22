import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Define the custom color palette
custom_palette = {
    "Licorice": "#251101",
    "Tyrian purple": "#470024",
    "Palatinate": "#5b1865",
    "YInMn Blue": "#2c5784",
    "Silver Lake Blue": "#5688c7"
}

# Convert the palette to a list of colors
colors = list(custom_palette.values())

# Create a custom colormap
custom_cmap = LinearSegmentedColormap.from_list("custom_palette", colors, N=256)

# Example usage with Matplotlib
import numpy as np

# Create some data
data = np.random.rand(10, 10)

# Plot using the custom colormap
plt.figure(figsize=(6, 6))
plt.imshow(data, cmap=custom_cmap)
plt.colorbar()
plt.title('Heatmap with Custom Color Palette')
plt.show()