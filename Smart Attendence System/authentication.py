import pandas as pd


def process_user_data(username, designation):
    titles_and_texts = []  # Will hold dynamic data
    if designation == "teacher":
        # Get files specific to the teacher
        g = get_files_from_matching_folder(
            "D:/DNN PROJECT 2024 MS-351/csv files/Login CSVS/student.csv (1).csv",
            username,
        )
        titles_and_texts = [
            {"title": f"{g[i]}", "text": f"{username}"} for i in range(len(g))
        ]
    elif designation == "student":
        # Extract student-specific data
        usernames, class_names = extract_usernames_and_classes(
            username, "D:/DNN PROJECT 2024 MS-351/csv files/students"
        )

        # Dynamically build the data for each class the student is enrolled in
        for i in range(len(class_names)):
            titles_and_texts.append(
                {
                    "title": class_names[i],
                    "text": f"Instructor Email: {usernames[i]}",
                }
            )

        print(titles_and_texts)
    return titles_and_texts


def extract_usernames_and_classes(email, student_file):
    # Extract the folder name from the email
    folder_name = email

    # Build the path to the folder
    folder_path = os.path.join(student_file, folder_name)

    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(
            f"Folder '{folder_name}' not found in the directory '{student_file}'"
        )

    # Find the CSV file in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

    if not csv_files:
        raise FileNotFoundError(f"No CSV file found in the folder '{folder_name}'")

    if len(csv_files) > 1:
        raise ValueError(
            f"Multiple CSV files found in the folder '{folder_name}'. Specify which one to use."
        )

    # Read the CSV file
    csv_file_path = os.path.join(folder_path, csv_files[0])
    df = pd.read_csv(csv_file_path)

    # Check for required columns
    if "username" not in df.columns or "class_name" not in df.columns:
        raise ValueError(
            f"The CSV file '{csv_files[0]}' must contain 'username' and 'class_name' columns."
        )

    # Extract all usernames and class_names
    usernames = df["username"].tolist()
    class_names = df["class_name"].tolist()

    # Ensure there is at least one entry
    if len(usernames) == 0 or len(class_names) == 0:
        raise ValueError("The CSV file does not contain enough data.")

    return usernames, class_names


def authentication_function(username, password, status):
    import pandas as pd

    status = status.lower()
    h = False

    if status == "student":
        df = pd.read_csv(
            "D:\DNN PROJECT 2024 MS-351\csv files\Login CSVS\student.csv (1).csv"
        )
        h = True
    elif status == "teacher":
        df = pd.read_csv("D:/DNN PROJECT 2024 MS-351/csv files/Login CSVS/teacher.csv")
        h = True
    else:
        return False  # Exit early if the status is invalid

    username = username.lower()
    password = str(password)  # Ensure password is treated as a string

    # Check if username and password match in the same row
    match = (
        (df["username"].str.lower() == username)
        & (df["password"].astype(str) == password)
    ).any()

    # Return the result based on matching rows and the valid status (h)
    return match


import os


def get_files_from_matching_folder(base_directory, folder_name_to_match):
    try:
        # Get a list of all folder names in the base directory
        folders = [
            folder
            for folder in os.listdir(base_directory)
            if os.path.isdir(os.path.join(base_directory, folder))
        ]

        # Check for a matching folder name
        matching_folder = next(
            (folder for folder in folders if folder_name_to_match in folder), None
        )

        if not matching_folder:
            return f"No folder matches the name: {folder_name_to_match}"

        # Get all file names in the matching folder
        folder_path = os.path.join(base_directory, matching_folder)
        file_names = [
            file
            for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file))
        ]

        return file_names

    except Exception as e:
        return f"An error occurred: {e}"


import os
import csv


def update_user_data(directory, instructor_name, email, username, reg):
    # Path to the instructor's folder
    instructor_folder = os.path.join(directory, instructor_name)

    # Check if the instructor's folder exists
    if not os.path.isdir(instructor_folder):
        raise FileNotFoundError(
            f"Folder for instructor '{instructor_name}' not found in the directory '{directory}'."
        )

    # Generate the file path for the class CSV file
    email_file_name = f"{email}.csv"
    email_file_path = os.path.join(instructor_folder, email_file_name)

    # Ensure the CSV file exists or create it with headers
    file_exists = os.path.isfile(email_file_path)

    # Read existing data to check if `reg` already exists
    if file_exists:
        try:
            with open(email_file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Reg"] == reg:
                        raise ValueError(
                            f"Duplicate entry found: reg '{reg}' already exists."
                        )
        except Exception as e:
            raise IOError(f"Error reading file '{email_file_name}': {e}")

    # Append the new data
    try:
        with open(email_file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Add header only if the file is new
            if not file_exists:
                writer.writerow(["Reg", "Name"])

            # Write the new data
            writer.writerow([reg, username])

    except Exception as e:
        raise IOError(f"Error updating file '{email_file_name}': {e}")


def create_or_append_user_data(base_directory, user_email, class_name, username):
    """
    Ensures a folder with the user's email exists, and appends username and class_name
    to the class_name.csv file inside it.

    Args:
        base_directory (str): The base directory where user folders are stored.
        user_email (str): The email of the user (used as folder name).
        class_name (str): The name of the class (used as CSV filename).
        username (str): The username to be added in the CSV file.
    """
    # Create the directory for the user
    user_directory = os.path.join(base_directory, user_email)
    os.makedirs(user_directory, exist_ok=True)  # Create the folder if it doesn't exist

    # Path to the class-specific CSV file
    class_file_path = os.path.join(user_directory, f"class_name.csv")

    # Check if the file exists
    file_exists = os.path.isfile(class_file_path)

    try:
        # Open the file in append mode
        with open(class_file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write header only if the file is new
            if not file_exists:
                writer.writerow(["username", "class_name"])

            # Append the new data
            writer.writerow([username, class_name])

        print(f"Data successfully added to {class_file_path}")

    except Exception as e:
        raise IOError(f"Error writing to file '{class_file_path}': {e}")
