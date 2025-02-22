    # Map class names to numeric class IDs
    class_id_mapping = {name: idx for idx, name in enumerate(class_names)}

    return class_names
def main_func_DNN_model_configuration():
    main_directory = "D:/DNN PROJECT 2024 MS-351/main_global_dataset_file"
    output_directory = "D:/DNN PROJECT 2024 MS-351/MTCNN_Applied_dataset_file"

    # Initialize MTCNN
    detector = MTCNN()

    # Define YOLO-specific paths
    images_train_dir = os.path.join(output_directory, "images/train")
    images_val_dir = os.path.join(output_directory, "images/val")
    labels_train_dir = os.path.join(output_directory, "labels/train")
    labels_val_dir = os.path.join(output_directory, "labels/val")

    # Ensure YOLO directories exist
    for path in [images_train_dir, images_val_dir, labels_train_dir, labels_val_dir]:
        os.makedirs(path, exist_ok=True)

    # List of class names (map these to numeric class IDs)
    class_names = get_class_names_from_directory("D:/DNN PROJECT 2024 MS-351/main_global_dataset_file")
    print(class_names)
    def process_image(image_path, img_output_dir, label_output_dir, student_label):
        """Process an image and save bounding boxes and YOLO annotations."""
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detections = detector.detect_faces(img_rgb)

        # Convert student_label to class ID
        class_id = class_names.index(student_label)  # Get the numeric class ID

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

        # Save the image in YOLO's image directory
        image_output_path = os.path.join(img_output_dir, os.path.basename(image_path))
        cv2.imwrite(image_output_path, img)

        # Save YOLO annotations in the labels directory
        annotation_file = os.path.join(
            label_output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}.txt"
        )
        with open(annotation_file, "w") as f:
            f.write("\n".join(yolo_annotations))

    # Split into train and validation sets
    train_ratio = 0.8
    all_images = []
    for student_dir in os.listdir(main_directory):
        student_path = os.path.join(main_directory, student_dir)
        if not os.path.isdir(student_path):
            continue
        for image_file in os.listdir(student_path):
            all_images.append(os.path.join(student_path, image_file))

    # Shuffle and split data
    np.random.shuffle(all_images)