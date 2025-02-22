import os
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
import shutil

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


def clear_directory(directory):
    """Delete all files and subdirectories within a directory."""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


def main_func_DNN_model_configuration():
    main_directory = "D:/DNN PROJECT 2024 MS-351/main_global_dataset_file"
    output_directory = "D:/DNN PROJECT 2024 MS-351/MTCNN_Applied_dataset_file"

    # Initialize MTCNN
    detector = MTCNN()
    print("Cleaning the output directory...")
    clear_directory(output_directory)
    print("Output directory cleaned successfully!")
    # YOLO-specific paths
    images_train_dir = os.path.join(output_directory, "images/train")
    images_val_dir = os.path.join(output_directory, "images/val")
    labels_train_dir = os.path.join(output_directory, "labels/train")
    labels_val_dir = os.path.join(output_directory, "labels/val")

    # Create necessary directories
    for path in [images_train_dir, images_val_dir, labels_train_dir, labels_val_dir]:
        os.makedirs(path, exist_ok=True)

    # Get class names
    class_names = get_class_names_from_directory(main_directory)
    if not class_names:
        print("No class names found. Check the dataset directory.")
        return

    def process_image(image_path, img_output_dir, label_output_dir, student_label):
        """Process an image and save bounding boxes and YOLO annotations."""
        # print(f"Processing Image: {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to read image: {image_path}")
            return  # Skip this image

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detections = detector.detect_faces(img_rgb)

        if not detections:
            print(f"No faces detected in: {image_path}")
            return

        class_id = class_names.index(student_label)  # Numeric class ID
        yolo_annotations = []
        for detection in detections:
            x, y, width, height = detection["box"]
            x_center = (x + width / 2) / img.shape[1]
            y_center = (y + height / 2) / img.shape[0]
            norm_width = width / img.shape[1]
            norm_height = height / img.shape[0]
            yolo_annotations.append(
                f"{class_id} {x_center} {y_center} {norm_width} {norm_height}"
            )

        # Save the processed image
        image_output_path = os.path.join(img_output_dir, os.path.basename(image_path))
        cv2.imwrite(image_output_path, img)
        print(f"Saved image to {image_output_path}")

        # Save YOLO annotations
        annotation_file = os.path.join(
            label_output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}.txt"
        )
        with open(annotation_file, "w") as f:
            f.write("\n".join(yolo_annotations))
        # print(f"Saved annotations to {annotation_file}")

    # Split into train and validation sets
    train_ratio = 0.9
    all_images = []
    for student_dir in os.listdir(main_directory):
        student_path = os.path.join(main_directory, student_dir)
        if not os.path.isdir(student_path):
            continue
        for image_file in os.listdir(student_path):
            image_path = os.path.join(student_path, image_file)
            if os.path.isfile(image_path):
                all_images.append(image_path)

    if not all_images:
        print("No images found in the dataset.")
        return

    np.random.shuffle(all_images)
    train_count = int(len(all_images) * train_ratio)
    train_images = all_images[:train_count]
    val_images = all_images[train_count:]

    # Process training images
    # print("Processing training images...")
    for image_path in train_images:
        student_label = os.path.basename(os.path.dirname(image_path))
        process_image(image_path, images_train_dir, labels_train_dir, student_label)

    # Process validation images
    # print("Processing validation images...")
    for image_path in val_images:
        student_label = os.path.basename(os.path.dirname(image_path))
        process_image(image_path, images_val_dir, labels_val_dir, student_label)

    print("MTCNN Training Data Configuration Completed Successfully!")
