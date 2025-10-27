############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
from tkinter import PhotoImage
from PIL import Image, ImageTk
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import shutil

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    os.makedirs(path, exist_ok=True)

##################################################################################

def tick():
    # Get the current time
    current_time = time.strftime('%I:%M:%S %p')
    
    # Update the clock label with the current time
    clock.config(text=current_time)
    
    # Schedule the next update after 1000 milliseconds (1 second)
    clock.after(1000, tick)


###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'dasdarshan7@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('comic', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('comic', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('comic', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('comic', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('comic', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('comic', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('comic', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#00fcca", height = 1,width=25, activebackground="white", font=('comic', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails")
    assure_path_exists("TrainingImage")

    filepath = os.path.join("StudentDetails", "StudentDetails.csv")
    # Create file if not exists
    if not os.path.isfile(filepath):
        with open(filepath, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(columns)

    # Count existing rows to get the next serial number
    with open(filepath, 'r') as csvFile:
        reader = list(csv.reader(csvFile))
        serial = len(reader)

    Id = txt.get()
    name = txt2.get()

    if not Id.isdigit():
        message.configure(text="ID must be numeric.")
        return

    if not name.replace(" ", "").isalpha():
        message.configure(text="Enter a valid name (letters and spaces only).")
        return

    user_folder = os.path.join("TrainingImage", f"{name}_{Id}")
    assure_path_exists(user_folder)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        message.configure(text="Failed to access camera.")
        return

    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    sampleNum = 0

    try:
        while True:
            ret, img = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                sampleNum += 1
                face_color = img[y:y + h, x:x + w]
                filename = f"{name}.{serial}.{Id}.{sampleNum}.jpg"
                cv2.imwrite(os.path.join(user_folder, filename), face_color)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('Taking Images (Press Q to quit)', img)

            
            key = cv2.waitKey(100) & 0xFF
            if key == ord('q') or key == ord('Q') or sampleNum >= 100:

                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

    # Save details to CSV
    with open(filepath, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([serial, '', Id, '', name])

        
    message1.configure(text=f"Images Taken for ID: {Id}")
    message.configure(text=f"Total Registrations till now : {serial}")

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel")

    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except AttributeError:
        message.configure(text="LBPH Recognizer not available. Install opencv-contrib-python.")
        return

    harcascadePath = os.path.join("haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(harcascadePath)

    faces, ID = getImagesAndLabels("TrainingImage")

    if not faces or not ID:
        messageboxshowerror("No Registrations", "Please register someone first!")
        return

    if len(faces) != len(ID):
        messagebox.showerror("Data Mismatch", "Mismatch between images and IDs.")
        return

    try:
        recognizer.train(faces, np.array(ID))
    except cv2.error as e:
        messagebox.showerror("Training Error", str(e))
        return

    recognizer.save(os.path.join("TrainingImageLabel", "Trainner.yml"))
    res = "Profile Trained & Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(len(set(ID))))

   
    
############################################################################################3

def getImagesAndLabels(path):
    faces = []
    IDs = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    imagePath = os.path.join(root, file)
                    pilImage = Image.open(imagePath).convert('L')  # Convert to grayscale
                    imageNp = np.array(pilImage, 'uint8')

                    # ID is expected at 2nd index based on filename format: name.serial.ID.sample.jpg
                    ID = int(file.split(".")[2])

                    faces.append(imageNp)
                    IDs.append(ID)
                except Exception as e:
                    print(f"[WARN] Skipping {imagePath}: {e}")

    return faces, IDs


###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return

    recognizer.read("TrainingImageLabel/Trainner.yml")
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']

    if not os.path.isfile("StudentDetails/StudentDetails.csv"):
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
        return

    df = pd.read_csv("StudentDetails/StudentDetails.csv")

    start_time = time.time()
    max_duration = 5  # seconds
    unknown_count = 0
    UNKNOWN_LIMIT = 10
    recorded_attendances = []
    seen_ids = set()  # NEW: to prevent duplicates

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p')

                name = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values

                if len(ID) == 0 or len(name) == 0:
                    continue  # skip if bad data

                ID = str(ID[0])
                name = str(name[0])

                if ID not in seen_ids:  # NEW: log only if not already seen
                    attendance = [ID, '', name, '', date, '', timeStamp]
                    recorded_attendances.append(attendance)
                    seen_ids.add(ID)

                bb = name
                unknown_count = 0  # reset unknown counter

            else:
                bb = 'Unknown'
                unknown_count += 1
                if unknown_count >= UNKNOWN_LIMIT:
                    print("Too many unknown faces detected. Exiting...")
                    cam.release()
                    cv2.destroyAllWindows()
                    return

            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)

        if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
            break

        if time.time() - start_time >= max_duration:
            print("Maximum capture time reached.")
            break

    # Save to CSV
    if recorded_attendances:
        date = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
        filename = f"Attendance/Attendance_{date}.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            if not file_exists:
                writer.writerow(col_names)
            for entry in recorded_attendances:
                writer.writerow(entry)

        with open(filename, 'r') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)  # skip header
            for i, row in enumerate(reader):
                id_val = row[0] + '   '
                tv.insert('', 0, text=id_val, values=(str(row[2]), str(row[4]), str(row[6])))

    cam.release()
    cv2.destroyAllWindows()


######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#2d420a')

# Load the background image
bg_image = Image.open("background_image1.png")
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the background image of the window
background_label = tk.Label(window, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame1 = tk.Frame(window, bg="#c79cff")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#c79cff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance Monitoring System" ,fg="white",bg="#2d420a" ,width=55 ,height=1,font=('comic', 29, ' bold '))
message3.place(x=10, y=10)

datef = tk.Label(window, text=day + "-" + mont[month] + "-" + year, fg="#ff61e5", bg="green",
                 width=20, font=('comic', 15, ' bold '))
datef.pack(fill='both', expand=True)
datef.place(relx=0.30, rely=0.09)

clock = tk.Label(window, fg="#ff61e5", bg="green", width=20, font=('comic', 15, ' bold '))
clock.place(relx=0.50, rely=0.09)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="#00fcca" ,font=('comic', 17, ' bold ') )
head2.place(x=0,y=-5)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="#00fcca" ,font=('comic', 17, ' bold ') )
head1.place(x=0,y=-5)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="#c79cff" ,font=('comic', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="#c79cff" ,font=('comic', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#c79cff" ,fg="black"  ,width=39 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#c79cff" ,fg="black"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="#c79cff"  ,height=1 ,font=('comic', 15, ' bold '))
lbl3.place(x=100, y=125)



res = 0
file_path = os.path.join("StudentDetails", "StudentDetails.csv")

if os.path.exists(file_path):
    with open(file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)  # Skip header
        for row in reader:
            if row and any(cell.strip() for cell in row):  # Skip empty rows
                res += 1
else:
    res = 0

message.configure(text='Total Registrations till now: ' + str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('comic', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

# Add horizontal scrollbar to Treeview
scroll_x = ttk.Scrollbar(frame1, orient='horizontal', command=tv.xview)
scroll_x.grid(row=3, column=0, pady=(0, 20), padx=(0, 100), sticky='ew')
tv.configure(xscrollcommand=scroll_x.set)


###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ff7221"  ,width=11 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ff7221"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=335, y=172)    
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="black"  ,bg="#3ffc00"  ,width=13  ,height=1, activebackground = "white" ,font=('comic', 12, ' bold '))
trackImg.place(x=160,y=85)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#eb4600"  ,width=10 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=400, y=460)

# Define a list of email domains
email_domains = ["gmail.com", "yahoo.com", "hotmail.com"]

# Function to send email
def send_email():
    recipient_email = recipient_email_entry.get()
    selected_domain = domain_var.get()

    if not recipient_email:
        mess._show(title='Error', message='Please enter a recipient email address.')
        return

    # Concatenate selected domain with recipient's email address
    recipient_email += "@" + selected_domain

    if not recipient_email:
        mess._show(title='Error', message='Please enter a recipient email address.')
        return

    from_email = from_email_entry.get()
    password = password_entry.get()

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient_email
    msg['Subject'] = "Today's Attendance Report , Date = " + date + ", Time = " + time.strftime('%I:%M:%S %p')

    body = "Please find attached the attendance report."
    msg.attach(MIMEText(body, 'plain'))

    filename = "Attendance\Attendance_" + date + ".csv"
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, recipient_email, text)
        server.quit()
        mess._show(title='Success', message='Attendance report sent successfully.')
    except Exception as e:
        print(e)
        mess._show(title='Error', message='Failed to send email. Please try again.')

# Add recipient email entry field
recipient_email_label = tk.Label(frame1, text="Recipient's Email", width=31, fg="black", bg="pink",
                                  font=('comic', 9, ' bold '))
recipient_email_label.place(x=6, y=30)
recipient_email_entry = tk.Entry(frame1, width=20, fg="black", bg="#d3f0dc", font=('comic', 15, ' bold '))
recipient_email_entry.place(x=5, y=50)


from_email_label = tk.Label(frame1, text="Sender's Email", width=31, fg="black", bg="pink",
                                  font=('comic', 9, ' bold '))
from_email_label.place(x=6, y=520)
from_email_entry = tk.Entry(frame1, width=20, fg="black", bg="#d3f0dc", font=('comic', 15, ' bold '))
from_email_entry.place(x=5, y=540)


password_label = tk.Label(frame1, text="Sender's Email Password", width=31, fg="black", bg="pink",
                                  font=('comic', 9, ' bold '))
password_label.place(x=261, y=520)
password_entry = tk.Entry(frame1, width=20, fg="black", bg="#d3f0dc", font=('comic', 15, ' bold '), show=('*'))
password_entry.place(x=260, y=540)

# Add domain dropdown menu
domain_label = tk.Label(frame1, text="Domain:", width=20, fg="black", bg="pink",
                                  font=('comic', 9, ' bold '))
domain_label.place(x=250, y=30)
domain_var = tk.StringVar(frame1)
domain_var.set(email_domains[0])  # Default domain
domain_dropdown = tk.OptionMenu(frame1, domain_var, *email_domains)
domain_dropdown.config(width=15, font=('comic', 9, ' bold '))
domain_dropdown.place(x=250, y=50)

# Add "@" symbol
at_symbol_label = tk.Label(frame1, text="@", width=2, fg="black", bg="white",
                                  font=('comic', 10, ' bold '))
at_symbol_label.place(x=230, y=50)

# Add send email button
send_email_button = tk.Button(frame1, text="Send Attendance", command=send_email, fg="black", bg="sky blue", width=13,
                              activebackground="white", font=('comic', 8, ' bold '))
send_email_button.place(x=400, y=50)

# Function to send email
def send_email():
    recipient_email = recipient_email_entry.get()
    selected_domain = domain_var.get()

    if not recipient_email:
        mess._show(title='Error', message='Please enter a recipient email address.')
        return

    # Concatenate selected domain with recipient's email address
    recipient_email += "@" + selected_domain

    if not recipient_email:
        mess._show(title='Error', message='Please enter a recipient email address.')
        return
    
def delete_registration_csv():
    registration_csv_path = "StudentDetails\StudentDetails.csv"
    if os.path.exists(registration_csv_path):
        os.remove(registration_csv_path)
        mess.showinfo("Success", "Registration CSV file deleted successfully.")
    else:
        mess.showinfo("Error", "Registration CSV file not found.")

def delete_attendance_csv():
    today = datetime.datetime.now().strftime('%d-%m-%Y')
    attendance_csv_path = f"Attendance\Attendance_{today}.csv"
    if os.path.exists(attendance_csv_path):
        os.remove(attendance_csv_path)
        mess.showinfo("Success", f"Attendance CSV file for {today} deleted successfully.")
    else:
        mess.showinfo("Error", f"Attendance CSV file for {today} not found.")

def open_attendance_folder():
    attendance_folder_path = "Attendance"
    if os.path.exists(attendance_folder_path):
        os.startfile(attendance_folder_path)
    else:
        mess.showinfo("Error", "Attendance folder not found.")

def open_todays_attendance_csv():
    today = datetime.datetime.now().strftime('%d-%m-%Y')
    todays_attendance_csv_path = f"Attendance\Attendance_{today}.csv"
    if os.path.exists(todays_attendance_csv_path):
        os.startfile(todays_attendance_csv_path)
        mess.showinfo("Success", f"Attendance CSV file for {today} opened successfully.")
    else:
        mess.showinfo("Error", f"Attendance CSV file for {today} not found.")


# Create buttons for deleting registration and attendance CSV files
delete_registration_button = tk.Button(frame1, text="Delete Registration CSV", command=delete_registration_csv, fg="white", bg="red", width=19, font=('comic', 8, 'bold'))
delete_registration_button.place(x=5, y=85)

delete_attendance_button = tk.Button(frame1, text="Delete Attendance CSV", command=delete_attendance_csv, fg="white", bg="red", width=19, font=('comic', 8, 'bold'))
delete_attendance_button.place(x=320, y=85)

# Button for Opening Attendance Folder & today's attendance csv file
open_attendance_button = tk.Button(frame1, text="Open Attendance Folder", command=open_attendance_folder,fg="white", bg="blue", width=19, font=('comic', 8, 'bold'))
open_attendance_button.place(x=5, y=115)

today = datetime.datetime.now().strftime('%d-%m-%Y')
open_todays_attendance_csv_button = tk.Button(frame1, text=(f"Open Today's Attendance CSV file, Dated - {today}"), command=open_todays_attendance_csv,fg="white", bg="green", width=50, font=('comic', 8, 'bold'))
open_todays_attendance_csv_button.place(x=5, y=460)


def delete_registered_images():
    """
    Deletes all registered images in the TrainingImage folder.
    """
    folder_path = "TrainingImage/"

    if os.path.exists(folder_path):
        try:
            # Delete the entire folder and its contents
            shutil.rmtree(folder_path)
            mess.showinfo("Success", "Registered images deleted successfully.")
        except Exception as e:
            mess.showinfo("Error", f"Failed to delete registered images: {e}")
    else:
        mess.showinfo("Error", "TrainingImage folder not found.")

# Create a button to delete registered images
delete_images_button = tk.Button(frame1, text="Delete Registered Images", command=delete_registered_images, fg="white", bg="red", width=20, font=('comic', 8, 'bold'))
delete_images_button.place(x=320, y=115)


window.configure(menu=menubar)
window.mainloop()


                 