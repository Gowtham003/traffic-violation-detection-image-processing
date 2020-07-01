import requests
from pprint import pprint
import cv2
import numpy as np
import os
from datetime import datetime, timedelta
import glob
import smtplib, ssl
import pandas as pd
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

global violated_data
violated_data=pd.DataFrame()
global temp_num
temp_num=[]

def detect_car(video_path, car_cascade_path, image_path, signal, date_time, address, stop_line_type):
    remove_files(image_path)
    min_area=5000
    path_temp=image_path+"temp"+".jpg"
    rectangles = []
    cap = cv2.VideoCapture(video_path)
    count = 0
    car_cascade = cv2.CascadeClassifier(car_cascade_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    count=signal["red_start_time"]*fps
    start=True
    temp_count=True
    green=False
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_pos = (50,50)
    fontScale = 1
    fontColor = (255,255,255)
    lineType = 2
    video_date_time=datetime.strptime(date_time, "%d/%m/%Y %H:%M:%S")
    ret, frames = cap.read()
    (hei ,wid, r) = frames.shape
    
    if stop_line_type=="near":
        line=[(0, int(0.6*hei)), (wid, int(0.6*hei))]
    elif stop_line_type=="far":
        line=[(0, int(0.3*hei)), (wid, int(0.3*hei))]
    elif stop_line_type=="medium":
        line=[(0, int(0.45*hei)), (wid, int(0.45*hei))]
    
    while cap.isOpened() :
        violated_in_frame=False
        ret, frames = cap.read()
        if ret:
            #cv2.imwrite('frame{:d}.jpg'.format(count), frame)
            #count += 15 # i.e. at 30 fps, this advances one second
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        else:
            cap.release()
            break
            
        if temp_count:
            count_temp=count
            temp_count=False
            
        (height ,width, r) = frames.shape
        
        """(line1, line2, line3, line4) = lines

        cv2.line(frames, line1[0], line1[1], (1, 1, 1), 3)
        cv2.line(frames, line2[0], line2[1], (1, 1, 1), 3)
        cv2.line(frames, line3[0], line3[1], (1, 1, 1), 3)
        cv2.line(frames, line4[0], line4[1], (1, 1, 1), 3)"""
        
        cv2.line(frames, line[0], line[1], (1, 1, 1), 3)
        
        """if signal["start_with"]=="yellow" and start:
            check=False
            start=False
            count+=(signal["yellow_duration"]+signal["green_duration"])*fps
            count=int(count/fps)*fps
            print(count/fps, "start with yellow")
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        elif signal["start_with"]=="green" and start:
            count+=signal["green_duration"]*fps
            count=int(count/fps)*fps
            print(count/fps, "start with green")
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            check=False
            start=False
        else:
            check=True"""
        check=True
        if check and int(count/fps)<int(count_temp/fps)+signal["red_duration"]:
            print(count/fps, "Red")
            gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 2, 1)

            """pts = np.array([line1[0],line1[1],line3[0],line3[1]])
            rect = cv2.boundingRect(pts)
            x,y,w,h = rect
            croped = frames[y:y+h, x:x+w].copy()

            pts = pts - pts.min(axis=0)

            mask = np.zeros(croped.shape[:2], np.uint8)
            cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

            ## (3) do bit-op
            violation_region = cv2.bitwise_and(croped, croped, mask=mask)"""
            
            violation_region=frames[line[0][1]:height, 0:width]
            rect=0, line[0][1], width, height-line[0][1]

            ## (4) add the white background
            #bg = np.ones_like(croped, np.uint8)*255
            #cv2.bitwise_not(bg,bg, mask=mask)
            #dst2 = bg+ dst

            #violation_region=frames[min(left_y1,right_y1) :max(right_y2, left_y2) , left_x1:(right_x2, right_x2)]
            #(vh, vw, re) = violation_region.shape
            #cv2.line(violation_region, (l_x2-line_x2, 0), (0, vh), (1, 1, 1), 3)
            for (x ,y ,w ,h) in cars:
                area=w*h
                center_x=int((2*x+w)/2)
                center_y=int((2*y+h)/2) 
                center=(center_x, center_y)
                """xp1=check_violation(line1, center)
                xp2=check_violation(line2, center)
                xp3=check_violation(line3, center)
                xp4=check_violation(line4, center)"""
                
                xp=check_violation(line, center)
                
                #if xp1>0 and xp2>0 and xp3>0 and xp4>0 and area>min_area:
                
                if xp>0 and area>min_area:
                    violated_in_frame=True
                    
            if violated_in_frame:
                cv2.imwrite(path_temp, violation_region)
                cv2.putText(frames,'Signal is Red - Checking Violations ', (50, 50), font, fontScale, fontColor, lineType)
                time_temp=video_date_time+timedelta(seconds=int(count/fps))
                cv2.putText(frames,str(time_temp), (width-450, 50), font, fontScale, fontColor, lineType)
                cv2.putText(frames,str(address), (width-450, height-50), font, fontScale, fontColor, lineType)
                plate_num=detectplate(path_temp, image_path, frames, rect)
                get_violated_data(plate_num, str(time_temp), address)
                #frames=resize_frame(frames)
                #cv2.imwrite(image_path+str(count)+".jpg", frames)
            count+=int(fps/2)
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
                
        else:
            temp_count=True
            #check=False
            green=True
        
            if green and check:
                count+=(signal["green_duration"]+signal["yellow_duration"])*fps
                count=int(count/fps)*fps
                print(count/fps, "green, yellow")
                cap.set(cv2.CAP_PROP_POS_FRAMES, count)
                green=False
            
            
        
        #cv2.imshow('video2', resized)        
        if cv2.waitKey(33) == 27 or count>=duration*fps:
            break
    cv2.destroyAllWindows()
    
    
def remove_files(image_path):
    files_in_dir = os.listdir(image_path)
    for f in files_in_dir:
        if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".csv"):
            os.remove(f'{image_path}{str(f)}')


def resize_frame(frames):
    (height, width, r)=frames.shape
    scale_percent = 70 # percent of original size
    width = int(width * scale_percent / 100)
    height = int(height * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(frames, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('video2', resized)  
    return frames


def detectplate(path_temp, image_path, frames, rect):
    global temp_num
    vehicle_data_list=list(vehicle_data["License Number"])
    plate_num=[]
    x, y, w, h = rect
    regions = ['gb', 'it']
    with open(path_temp, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            #data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token your_token'})
    Result=response.json()
    fp=cv2.imread(path_temp)
    if len(Result['results'])>0:
        for i in range(len(Result['results'])):
            temp_frame=frames.copy()
            plate=str(Result['results'][i]['plate'])
            score=Result['results'][i]['region']['score']
            plate=plate.upper()
            print(plate, score)
            if len(plate)==6 and plate in vehicle_data_list and plate not in temp_num:
                temp_num.append(plate)
                ymin=Result['results'][i]['box']['ymin']
                xmin=Result['results'][i]['box']['xmin']
                ymax=Result['results'][i]['box']['ymax']
                xmax=Result['results'][i]['box']['xmax']
                cv2.rectangle(temp_frame, (xmin+x-30, ymin+y-30), (xmax+x+30, ymax+y+30),(255 ,0 ,0) ,2)
                cv2.imwrite(image_path+plate+".jpg", temp_frame)
                plate_num.append(plate)
    os.remove(path_temp)
    return plate_num


def check_violation(line, center):
    (center_x, center_y) = center
    (l_x1, l_y1), (l_x2, l_y2) = line
    v1 = (l_x2-l_x1, l_y2-l_y1)   
    v2 = (l_x2-center_x, l_y2-center_y)   
    xp = v1[0]*v2[1] - v1[1]*v2[0]
    return xp


def get_violated_data(plate_num, time_temp, address):
    for num in plate_num:
        vehicle_data_list=list(vehicle_data["License Number"])
        #vehicle_data[vehicle_data["License Number"].str.contains(num)]
        index=vehicle_data_list.index(num)
        #index=vehicle_data[vehicle_data["License Number"]==num].index.item()
        vehicle_type=vehicle_data.loc[index]["Vehicle Type"]
        e_mail_id=vehicle_data.loc[index]["E-mail"]
        name=vehicle_data.loc[index]["Name"]
        ph_num=vehicle_data.loc[index]["Phone Number"]
        vehicle_data.at[index, 'Total number of Violations']=int(vehicle_data.loc[index]["Total number of Violations"])+1
        no_of_violations=vehicle_data.loc[index]["Total number of Violations"]
        violations_allowed=vehicle_data.at[index, 'Violations Allowed']
        global violated_data
        if violated_data.empty==True:
            violated_data=pd.DataFrame([(num, name, vehicle_type, address, time_temp, e_mail_id, ph_num, no_of_violations, violations_allowed)], columns=["License Number", "Owner_Name", "Vehicle Type", "Violated Signal", "Date & Time", "E-mail", "Phone Number", "Total number of Violations", 'Violations Allowed'])
        else:
            temp_list=list(violated_data["License Number"])
            if num in temp_list:
                ind=temp_list.index(num)
                violated_data=violated_data.drop(violated_data.index[ind])
            violated_data=violated_data.append(pd.Series([num, name, vehicle_type, address, time_temp, e_mail_id, ph_num, no_of_violations, violations_allowed], index=violated_data.columns), ignore_index=True)


def send_mails(port, smtp_server, sender_email, password, image_path):
    print("Sending Mails")
    s = smtplib.SMTP(smtp_server, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sender_email, password)
    for index, row in violated_data.iterrows():
        if row['Violations Allowed']=='NO':
            e_mail=row["E-mail"]
            address=row["Violated Signal"]
            license_number=row["License Number"]
            owner_name=row["Owner_Name"]
            date_time=row["Date & Time"]
            vehicle_type=row["Vehicle Type"]
            no_of_violations=row["Total number of Violations"]
            img_data = open(image_path+license_number+".jpg", 'rb').read()
            msg = MIMEMultipart()
            msg['Subject'] = 'Traffic Signal Violation Alert'
            #msg['From'] = 'e@mail.cc'
            #msg['To'] = 'e@mail.cc'

            text = MIMEText("Hi "+owner_name+", Your "+vehicle_type+" with license number "+license_number+" was violated totally "+str(no_of_violations)+" times in a traffic signal. This time the violation is at "+address+" on "+date_time)
            msg.attach(text)
            image = MIMEImage(img_data, name=os.path.basename(image_path+license_number.lower()+".jpg"))
            msg.attach(image)
            
            s.sendmail(sender_email, e_mail, msg.as_string())
    s.quit()


def start_checking(video_path, red_start_time, red_duration, green_duration, yellow_duration, date_time, stop_line_type):
    car_cascade_path='./videoreport/static_files/cascade/cars1.xml'
    licence_cascade_path='./videoreport/static_files/cascade/cascade_licence_plate_1.xml'
    image_path='./videoreport/static_files/Violated_cars/'

    signal={"red_start_time": int(red_start_time), "red_duration": int(red_duration), "green_duration": int(green_duration), "yellow_duration": int(yellow_duration)}

    address="Old Bus Stand Salem"

    date_time=date_time # should be in this format -> "%d/%m/%Y %H:%M:%S"

    stop_line_type=stop_line_type #near, far, medium

    data_path="./videoreport/static_files/vehicle_data/vehicle_database.csv"
    global vehicle_data
    vehicle_data=pd.read_csv(data_path, index_col=0)
    vehicle_data.drop(vehicle_data.columns[vehicle_data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    global temp_num
    temp_num=[]
    
    detect_car(video_path, car_cascade_path, image_path, signal, date_time, address, stop_line_type)

    port = 587  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "your_mail_id@gmail.com"  # Enter your address
    password = "your_password"

    send_mails(port, smtp_server, sender_email, password, image_path)
    
    global violated_data
    violated_data.to_csv(image_path+"violated_data.csv")
    vehicle_data.to_csv(data_path)
    
    