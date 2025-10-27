# Face-recognition-based--attendence-monitoring-system
🧠 Face Recognition Attendance System
📋 Project Overview

This project is a Face Recognition-based Attendance System built using Python, OpenCV, and Tkinter GUI.
It captures student faces, trains the model using the LBPH Face Recognizer, and automatically marks attendance when faces are recognized.
It also allows the admin to send attendance reports via email and manage stored records easily.

🚀 Features

✅ GUI Interface (Tkinter) – User-friendly interface for managing attendance.
✅ Face Registration – Capture and store student face images.
✅ Training Module – Trains the LBPH model for accurate recognition.
✅ Real-time Face Detection – Marks attendance automatically through the webcam.
✅ Attendance Export – Saves daily attendance as a .csv file.
✅ Email Integration – Sends attendance reports directly through email.
✅ Password Protection – Protects training and admin features.
✅ Data Management – Options to delete or open attendance/registration files.


🧩 Technologies Used

Python 3.x

OpenCV (cv2)

Tkinter

Pandas & NumPy

PIL (Pillow)

smtplib (for Email Sending)

CSV for data storage



📁 Project Structure
Face_Recognition_Attendance_System/
│
├── Face_Recognition_Attendance_System.py
├── haarcascade_frontalface_default.xml
├── background_image1.png
│
├── TrainingImage/                 # Stores captured face images
├── TrainingImageLabel/            # Stores trained model and password file
├── StudentDetails/                # Stores student info (StudentDetails.csv)
├── Attendance/                    # Stores attendance CSV files
│
└── README.md


⚙️ How to Run
1️⃣ Install Required Libraries
pip install opencv-python opencv-contrib-python pillow pandas numpy

2️⃣ Clone or Download 

3️⃣ Add Required Files

Place haarcascade_frontalface_default.xml and background_image1.png in the same directory as the main .py file.

4️⃣ Run the Application
python Face_Recognition_Attendance_System.py




 How It Works

Register New User:
Enter ID and Name → Click “Take Images” → System captures 100 face samples.

Train Model:
Click “Save Profile” → System trains and stores the model.

Take Attendance:
Click “Take Attendance” → Webcam recognizes faces and logs attendance.

Email Report (Optional):
Fill sender & receiver email → Click “Send Attendance”.

Manage Data:
Delete, open, or view attendance and registration CSV files easily.



🛡️ Security

Password-protected access for model training.

Option to change admin password securely.


🧑‍💻 Author

Developed by: Mohit yadav
📧 Email: mohityadav4504@gmail.com
]
💻 GitHub: 

