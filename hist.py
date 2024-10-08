import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy
from util import *
from setup import *

import imageio
from matplotlib.colors import ListedColormap


# rbgs = [
#     (0.0, 0.6056031611752245, 0.9786801175696073),
#     (0.8888735002725197, 0.4356491903481899, 0.2781229361419437),
#     (0.2422242978521988, 0.6432750931576305, 0.3044486515341153),
#     (0.7644401754934357, 0.44411177946877667, 0.8242975359232757),
#     (0.6755439572114058, 0.5556623322045815, 0.09423433626639476),
#     (4.821181565883848e-7, 0.6657589812923558, 0.6809969518707946),
#     (0.930767491919665, 0.3674771896571418, 0.5757699667547833),
#     (0.7769816661712935, 0.5097431319944512, 0.1464252569555494),
#     (3.8077343912812365e-7, 0.6642678029460113, 0.5529508754522481),
#     (0.558464964115081, 0.5934846564332881, 0.11748125233232112),
#     (5.947623876556563e-7, 0.6608785231434255, 0.7981787608414301),
#     (0.6096707676128643, 0.49918492100827794, 0.9117812665042643),
#     (0.3800016049820355, 0.5510532724353505, 0.9665056985227145),
#     (0.9421816479542178, 0.37516423354097606, 0.4518168202944591),
#     (0.8684020893043973, 0.3959893639954848, 0.7135147524811882),
#     (0.423146743646308, 0.6224954944199984, 0.1987706025213047),
# ]
# juliacmaps = ListedColormap(rbgs)
# Configure rcParams to use LaTeX and serif font
# colors = juliacmaps(np.linspace(0, 1, len(rbgs)))  # Get all colors from the colormap
# plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)

plt.rcParams.update(
    {
        "text.usetex": False,  # Use LaTeX for text rendering
        "font.family": "serif",  # Use serif font family
        "font.serif": [
            "Computer Modern Roman"
        ],  # Specify specific serif font (default LaTeX font)
        # 'axes.labelsize': 12,  # Font size for labels
        "font.size": 28,  # General font size
        "legend.fontsize": 28,  # Font size for legend
        "xtick.labelsize": 28,  # Font size for x-axis ticks
        "ytick.labelsize": 28,  # Font size for y-axis ticks
        # "image.cmap": "juliacmaps",  # Set custom colormap
    }
)

# Replace with your MySQL connection details
engine = sqlalchemy.create_engine(
    "mysql+pymysql://root:19931017@127.0.0.1:3306/cutest", echo=True
)

# Load data from MySQL
UNSELECT_METHOD2 = r"('\\galahadarc')"
query = f"""
SELECT name, method, kg, n, `update` FROM result
where `precision` = 1e-5
            and method not in {UNSELECT_METHOD}
            and method not in {UNSELECT_METHOD2}
            and 500 <= n <= 5000
"""
with engine.begin() as conn:
    df = pd.read_sql(query, con=engine)

# Sort by 'update' to ensure the most recent entries are at the top
df_sorted = df.sort_values(by="update", ascending=False)


# plot the ratio
# Select the most recent entry for each method using drop_duplicates on 'method'
df_sorted = df_sorted.drop_duplicates(subset=["name", "method"], keep="first")

# Ensure every method has an entry for each name
methods = df_sorted["method"].unique()
names = df_sorted["name"].unique()

# Reindex the DataFrame to fill missing method-name combinations
df_filled = (
    df_sorted.set_index(["name", "method"])
    .unstack(fill_value=np.nan)
    .stack()
    .reset_index()
)

# Fill missing kg values with 2^5 where names are missing for a method
df_filled["kg"].fillna(2**5, inplace=True)

# Calculate the minimum (best) kg for each name
df_filled["best_kg"] = df_filled.groupby("name")["kg"].transform("min")

# Calculate the ratio of kg to the minimum kg for the same name
df_filled["kg_ratio"] = df_filled["kg"] / df_filled["best_kg"]

# Create a figure
plt.figure(figsize=(10, 6))

# Plot the ratio for each method
for method in methods:
    method_data = df_filled[df_filled["method"] == method]  # Filter by method

    # Plot the kg ratio vs name
    plt.scatter(
        range(len(method_data["name"])),
        method_data["kg_ratio"],
        marker="o",
        label=method,
    )

# Set log scale for y-axis
plt.yscale("log")

# Customize the plot
plt.xlabel("")  # Hide x-axis labels (name)
plt.ylabel("Ratio to best $k_g$")  # Set y-axis label
# plt.title("kg Ratio vs Name for Each Method (Most Recent Entry)")
plt.legend(title="Method")
plt.xticks([])  # Hide x-axis ticks for name
plt.tight_layout()

# Show the plot
plt.show()
