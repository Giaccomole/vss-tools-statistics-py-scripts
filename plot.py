import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import yaml
import numpy as np

from anytree import PreOrderIter, PostOrderIter

# from vss_tools.model import VSSDataBranch, VSSDataDatatype
# from vss_tools.tree import VSSNode

from rich.pretty import pretty_repr

# ####################

# def is_VSS_leaf(node: VSSNode) -> bool:
#     """Check if the node is a VSS leaf (i.e., one of VSS sensor, attribute, or actuator)"""
#     if isinstance(node.data, VSSDataDatatype):
#         return True
#     return False

# def is_VSS_branch(node: VSSNode) -> bool:
#     """Check if the node is a VSS branch (and not an instance branch)"""
#     if isinstance(node.data, VSSDataBranch):
#         if not node.data.is_instance:
#             return True
#     return False

# def is_VSS_branch_instance(node: VSSNode) -> bool:
#     """Check if the node is a VSS branch instance)"""
#     if isinstance(node.data, VSSDataBranch):
#         if node.data.is_instance:
#             return True
#     return False

# #####################


def load_yaml_data(file_path):
    """
    Load data from a YAML file.

    :param file_path: Path to the YAML file containing the vehicle data.
    :return: Data loaded from the YAML file
    """
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        print(f"Error loading YAML data: {e}")
        return None


def count_types(data):
    """
    Count the occurrences of each 'type' in the YAML data.

    :param data: The loaded YAML data.
    :return: A dictionary with the count of each type.
    """
    type_counts = {"actuator": 0, "sensor": 0, "attribute": 0, "branch": 0}

    def recursive_count(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and "type" in value:
                    if value["type"] in type_counts:
                        type_counts[value["type"]] += 1
                recursive_count(value)

    recursive_count(data)
    return type_counts

custom_palette = {
    "Licorice": "#251101",
    "Tyrian purple": "#470024",
    "Palatinate": "#5b1865",
    "YInMn Blue": "#2c5784",
    "Silver Lake Blue": "#5688c7"
}

colors = list(custom_palette.values())

custom_cmap = LinearSegmentedColormap.from_list("custom_palette", colors, N=256)


def plot_data(type_counts):
    """
    Plot the count of each type in a bar chart with numbers on the bars and colorful bars.

    :param type_counts: A dictionary containing the count of each type.
    """
    types = list(type_counts.keys())
    counts = list(type_counts.values())

    colors = custom_cmap(np.linspace(0, 1, len(types)))

    plt.figure(figsize=(8, 6))
    bars = plt.bar(types, counts, color=colors)

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            int(yval),
            ha="center",
            va="bottom",
            fontsize=12,
        )

    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.title("Number of Each Type in the Vehicle Signal Specification")

    plt.tight_layout()
    plt.show()


def main():
    yaml_file_path = "VehicleSignalSpecification.yaml"

    print(f"Loading data from YAML file: {yaml_file_path}...")
    data = load_yaml_data(yaml_file_path)

    if data:
        print("Data loaded successfully. Counting types...")
        type_counts = count_types(data)
        print("Type counts:", type_counts)
        print("Plotting data...")
        plot_data(type_counts)
    else:
        print("Failed to load data.")


if __name__ == "__main__":
    main()
