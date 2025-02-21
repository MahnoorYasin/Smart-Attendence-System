# **Smart Attendance System**  

## **📌 Introduction**  
The **Smart Attendance System** is an AI-powered solution that automates attendance marking using **computer vision** and **deep learning**. It eliminates the inefficiencies of traditional methods by offering a **real-time, error-free, and scalable** attendance management system. This system is designed for **schools, offices, and events** to streamline attendance tracking with **high accuracy**.  

## **🔍 Features**  
✅ **Automated Face Recognition** – Uses **MTCNN** for face detection and **YOLOv8** for person identification.  
✅ **Real-Time Attendance Marking** – Automatically logs attendance in a **CSV file or database**.  
✅ **Secure & Scalable** – Can be expanded for large organizations.  
✅ **User-Friendly Interface** – Built with **HTML, CSS, and Flask** for smooth operation.  

## **🛠️ Technologies Used**  
- **Deep Learning Models**: YOLOv8 (Object Detection), MTCNN (Face Detection)  
- **Backend**: Flask (Python)  
- **Frontend**: HTML, CSS  
- **Database**: CSV for attendance storage  
- **Libraries**: OpenCV, NumPy, Pandas, TensorFlow  

## **📂 Dataset**  
The dataset consists of **45 student images**, each stored in individual folders with corresponding **CSV files** containing student details. The images are labeled for model training, ensuring accurate identification.  

## **⚙️ System Workflow**  
1️⃣ **Admin Login** – The admin logs in through `index.html`.  
2️⃣ **Class Selection** – The admin selects a class from `Class list.html`.  
3️⃣ **Face Recognition** – The system detects faces and marks attendance.  
4️⃣ **Attendance Update** – The `Main display class.html` page shows real-time attendance updates.  

## **📌 Installation Guide**  
### **🔹 Prerequisites**  
Ensure you have the following installed:  
- Python 3.x  
- Flask  
- OpenCV  
- NumPy  
- TensorFlow  
- Pandas  

### **🔹 Setup Instructions**  
1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/MahnoorYasin/Smart-Attendance-System.git
cd Smart-Attendance-System
```  
2️⃣ **Install Dependencies**  
```sh
pip install -r requirements.txt
```  
3️⃣ **Run the Flask Server**  
```sh
python app.py
```  
4️⃣ **Open in Browser**  
Visit `http://127.0.0.1:5000/` to access the system.  
