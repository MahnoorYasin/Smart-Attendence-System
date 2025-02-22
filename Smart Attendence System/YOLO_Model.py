import subprocess
from ultralytics import YOLO, __version__
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Print Ultralytics version
print(f"Ultralytics version: {__version__}")

# Load the model
model = YOLO("yolov8s.pt")

# Print model architecture
print(model.model)

# Train the model
results = model.train(
    data="D:/DNN PROJECT 2024 MS-351/data.yaml",
    epochs=25,
    imgsz=800,
    batch=2,
    verbose=True,
    plots=True,
    amp=True,
    cos_lr=True,
    pretrained=False,
)

# Save the results
print("Training Results:", results)
