from mtcnn.mtcnn import MTCNN
from flask import send_from_directory
from flask import Flask, request, render_template, redirect, url_for, jsonify,Response, make_response
from flask import send_file, abort
import os
import cv2
import pandas as pd
import datetime
import csv
import numpy as np
import time
import zipfile
import os
from comparison import main_
from yaml_creation import func_yaml
from prediction import detect_and_log
from main_dataset_configurartion import main_func_DNN_model_configuration
from authentication import (
    update_user_data,authentication_function,
    create_or_append_user_data,
    get_files_from_matching_folder,
    process_user_data,
)  # Your external authentication logic

# Making a flask app
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    print("We are currently on the login page")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        designation = request.form["designation"]
        print("POST")
        approval_status = authentication_function(username, int(password), designation)
        if approval_status:
            titles_and_texts = process_user_data(username, designation)
            print(titles_and_texts)
            return render_template(
                "Main_display_class.html",
                classes=titles_and_texts,
            )
        else:
            # If authentication fails, pass an error message to the template
            return render_template("index.html", error_message="Invalid username, password, or designation.")

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    # Retrieve the uploaded file and class/instructor names
    uploaded_file = request.files.get("file")
    class_name = request.form.get("class_name")
    instructor_name = request.form.get("class_name_")

    if uploaded_file and class_name and instructor_name:
        try:

            # print(instructor_name)
            # print(class_name)
            original_string = instructor_name
            updated_string = original_string.replace("Instructor Email: ", "")
            instructor_name = updated_string
            # Define base paths for saving files
            base_save_path = r"D:/DNN PROJECT 2024 MS-351/main_uploading_folder/"
            # class_save_path = os.path.join(base_save_path, class_name)
            base = r"D:/DNN PROJECT 2024 MS-351/csv files/Instructor/"
            path = os.path.join(base, instructor_name)
            path_main = os.path.join(path, class_name) + ".csv"
            print(path_main)
            # Ensure the necessary directories exist
            # os.makedirs(class_save_path, exist_ok=True)
            os.makedirs(path, exist_ok=True)

            # Define the file path and save the file
            file_path = os.path.join(base_save_path, uploaded_file.filename)
            uploaded_file.save(file_path)
            

            # Print out debugging info (can be replaced with logging)
            print(f"path_main: {path_main}")
            # print(f"Saved to: {file_path}")
            # print(f"Class save path: {class_save_path}")
            print(f"Base save path: {file_path}")
            
            detect_and_log(file_path)
            # Call your processing function (ensure it's defined correctly)
            main_(path_main, "D:/DNN PROJECT 2024 MS-351/csv files/classes_list/l.csv")
            
            return f"File '{uploaded_file.filename}' uploaded successfully for class '{class_name}'!"

        except Exception as e:
            return f"An error occurred: {e}"

    return "No file, class name, or instructor name provided."


@app.route("/class_list", methods=["POST", "GET"])
def check_and_display():
    import os

    # Path to the folder
    folder_path = "D:/DNN PROJECT 2024 MS-351/csv files/Instructor/ali.nasir@gmail.com"

    # Initialize an empty dictionary to store file names and their content
    file_data = {}

    # Check if the folder contains any files
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not files:
        # If no files found, pass an empty list and a message
        return render_template(
            "class_list.html", file_data=None, message="No files found in the folder."
        )
    else:
        # Read the contents of each file
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()  # Read file content
                file_data[file] = content

        # Pass the file names and content to the template
        return render_template("class_list.html", file_data=file_data, message=None)


@app.route("/download", methods=["POST","GET"])
def download_file():
    # Define the file directory (only directory path, no filename here)
    directory = r"D:/DNN PROJECT 2024 MS-351/csv files/Login CSVS"  # Directory where the file is stored
    filename = "student.csv (1).csv"  # The filename you want to send

    class_text = request.form.get("class_text")
    class_name2 = request.form.get("class_name2")

    # Debugging: Print the retrieved values
    print(f"Class Text: {class_text}")
    print(f"Class Name: {class_name2}")
    try:
        # Use send_from_directory to send the file for download
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found.", 404


import os
import zipfile
import time


@app.route("/register", methods=["GET", "POST"])
def register_user():
    # Path to your CSV file
    csv_file_path = (
        "D:/DNN PROJECT 2024 MS-351/csv files/Login CSVS/student.csv (1).csv"
    )

    if request.method == "POST":

        # Retrieve form data
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        instructor_name = request.form.get("IN")
        class_name = request.form.get("CN")
        reg = request.form.get("reg")
        main_directory = "D:/DNN PROJECT 2024 MS-351/csv files/Instructor"
        base_directory = "D:/DNN PROJECT 2024 MS-351/csv files/students"

        # Ensure all required fields are provided
        if (
            not email
            or not password
            or not username
            or not instructor_name
            or not class_name
            or not reg
        ):
            return "All fields are required!", 400

        # Update instructor data and create or append student data
        try:
            update_user_data(main_directory, instructor_name, class_name, username, reg)
            create_or_append_user_data(
                base_directory, email, class_name, instructor_name
            )
        except:
            print("Error 156")

        # Save email and password to CSV
        file_exists = os.path.isfile(csv_file_path)
        try:
            with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # If the file doesn't exist, write the header
                if not file_exists:
                    writer.writerow(["username", "password"])

                # Write user data
                writer.writerow([email, password])
        except Exception as e:
            return f"Error writing to CSV: {e}", 500

        # Handle file upload
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename.endswith(".zip"):
            # Save and process file
            file_path = os.path.join(
                "D:/DNN PROJECT 2024 MS-351/csv files/New_User_photos",
                uploaded_file.filename,
            )
            uploaded_file.save(file_path)

            extract_folder = os.path.join(
                "D:/DNN PROJECT 2024 MS-351/main_global_dataset_file"
            )
            os.makedirs(extract_folder, exist_ok=True)

            # Extract the ZIP file without creating extra subdirectories
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                for file in zip_ref.namelist():
                    # Extract files directly into the username folder (avoid creating an extra folder)
                    zip_ref.extract(file, extract_folder)

                    # Optionally, you can filter to extract only images (e.g., .jpg, .png files)
                    if file.endswith((".jpg", ".png",".jpeg")):
                        print(f"Extracted {file}")

            os.remove(file_path)  # Cleanup uploaded zip file
            return f"User {username} registered and files uploaded successfully!"

        return "Please upload a valid zip file containing your photos."

    return render_template("New_user_registration_form.html")

@app.route("/Trainer", methods=["POST", "GET"])
def MTCNN_TRAINER():
    try:
        # Call the required functions
        print("Starting DNN Model Configuration...")
        main_func_DNN_model_configuration()
        print("DNN Model Configuration Completed.")

        print("Starting YAML Configuration...")
        func_yaml()
        print("YAML Configuration Completed.")

        # Return the registration form page with a success message
        return render_template("New_user_registration_form.html", message="Trainer successfully activated!")
    except Exception as e:
        # Return an error message if something goes wrong
        print(f"Error in MTCNN_TRAINER: {e}")
        return render_template("New_user_registration_form.html", error_message="An error occurred while activating the trainer.")


@app.route("/courselist", methods=["POST", "GET"])
def index():
    # List all folders and their files
    BASE_DIR = "D:/DNN PROJECT 2024 MS-351/csv files/Instructor"
    folder_file_data = {}

    for root, dirs, files in os.walk(BASE_DIR):
        folder = os.path.basename(root)
        if files:  # Only add folder if it contains files
            # Use os.path.splitext to remove extensions
            folder_file_data[folder] = [os.path.splitext(file)[0] for file in files]

    # Render the template and pass the folder and file data
    return render_template("form_instructor_detail.html", folder_file_data=folder_file_data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
