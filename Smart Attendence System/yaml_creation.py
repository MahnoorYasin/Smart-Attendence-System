import os
import pandas as pd
import numpy as np


def get_class_names_from_directory(directory_path):
    # List all folders in the directory
    class_names = [
        name
        for name in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, name))
    ]

    # Sort class names (optional for consistency)
    class_names.sort()

    # Count the number of classes
    num_classes = len(class_names)

    # Map class names to numeric class IDs (optional, not used in this case)
    class_id_mapping = {name: idx for idx, name in enumerate(class_names)}

    # Return both class names and the number of classes
    return class_names, num_classes


def func_yaml():
    # Get the class names and number of classes
    d, f = get_class_names_from_directory("D:/DNN PROJECT 2024 MS-351/main_global_dataset_file")

    # Format the class names list as a string with double quotes
    class_names_str = "[" + ", ".join([f'"{name}"' for name in d]) + "]"

    # Prepare YAML content using f-string formatting
    data_yaml_content = f"""
    train: 'D:/DNN PROJECT 2024 MS-351/MTCNN_Applied_dataset_file/images/train'
    val: 'D:/DNN PROJECT 2024 MS-351/MTCNN_Applied_dataset_file/images/val'

    nc: {f}
    names: {class_names_str}
    """

    # Write the content to a .yaml file
    with open("data.yaml", "w") as file:
        file.write(data_yaml_content)

# func_yaml()