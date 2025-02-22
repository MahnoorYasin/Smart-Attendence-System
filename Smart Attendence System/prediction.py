import pandas as pd
from ultralytics import YOLO
import os


def get_class_names_from_directory(directory_path):
    """Retrieve class names from the directory."""
    class_names = [
        name
        for name in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, name))
    ]
    class_names.sort()
    print(f"Class Names Found: {class_names}")
    return class_names


def detect_and_log(image_path):
    # Path to the trained YOLO model
    model_path = "D:/DNN PROJECT 2024 MS-351/best (1) (1).pt"

    # Define the persons you're interested in detecting (with spaces in names)
    class_names = [
        "Abdullah Awan",
        "Ahsan Saleem",
        "Ali Gohar",
        "Asad Irfan",
        "Hashim Rabnawaz",
        "Hassan Wadood",
        "Karar Ahmed",
        "Kashif Mehmood",
        "Khizar",
        "Maaz Hamid",
        "Mamoon Rashid",
        "Maqsood Ahmed",
        "Mustafa",
        "Qasim",
        "Saifullah Saleem",
        "Yasir Jamal",
    ]

    # Path to the CSV file where results will be stored
    csv_file = "D:/DNN PROJECT 2024 MS-351/csv files/classes_list/l.csv"

    # Check if the provided image file exists
    if os.path.exists(image_path):
        # Load the trained YOLO model
        model = YOLO(model_path)

        # Run prediction
        results = model.predict(image_path, imgsz=800)

        # Initialize a dictionary to store detection status for each person
        detection_status = {name: "A" for name in class_names}

        # Iterate through the results (results is a list, so we access the first result)
        for result in results:
            # Get the class names and boxes for the detected objects
            class_names_in_image = result.names  # Mapping class ids to class names
            boxes = result.boxes.xywh  # Bounding boxes (xywh format)

            # Iterate over the detections
            for i, box in enumerate(boxes):
                class_id = result.boxes.cls[i].item()  # Get the class ID
                class_name = class_names_in_image[
                    class_id
                ]  # Get the class name from the ID

                # Update the detection status if the class name is in the list
                if class_name in detection_status:
                    detection_status[class_name] = "P"  # Mark as present (P)

        # Prepare the data in the required format
        data = [
            {"Name": name, "Status": status}
            for name, status in detection_status.items()
        ]

        # Convert the list of dictionaries to a DataFrame
        df_result = pd.DataFrame(data)

        # Check if the file exists and delete its content (clear the file)
        if os.path.exists(csv_file):
            os.remove(csv_file)  # Delete the existing file

        # Write the new data to the CSV file
        df_result.to_csv(csv_file, mode="w", header=True, index=False)

        # Display the results (for debugging)
        print(df_result)

        # Delete the processed image after prediction
        os.remove(image_path)
        print(f"Image {image_path} has been deleted after processing.")
    else:
        print("The provided image file does not exist.")


# detect_and_log('c:/Users/dell/Downloads/DNN Project-20241216T151705Z-001/DNN Project/Maaz Hamid/WhatsApp Image 2024-12-10 at 9.25.18 PM(1).jpeg')