import datetime
import os
import time
import csv

import cv2
import pandas as pd

#-------------------------
def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read(r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv(r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\StudentDetails"+os.sep+"StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    #col_names = ['Id', 'Name', 'Date', 'Time']
    #attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  #  video width
    cam.set(4, 480)  #  video height
    
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 100:
                aa = df.loc[df['Id'] == Id]['Name'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa


            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            if (100-conf) > 60:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = str(aa)[2:-2]
                row = [Id, aa, date, timeStamp]
                data = pd.read_csv(r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\Attendance\Attendance.csv")
                id_list = data['Id'].tolist()
                date_list = data['Date'].tolist()
                n = 0
                for i in range(0,len(id_list)-1):
                    if id_list[i]== Id :
                        n=n+1
                
                if n==0:
                    with open(r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\Attendance\Attendance.csv", 'a+') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                            
        

            tt = str(tt)[2:-2]
            if(100-conf) > 60:
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

            if (100-conf) > 60:
                cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
           
            elif (100-conf) > 50:
                cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 255), 2)
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
           
            else:
                cv2.rectangle(im, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)


        #attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    #date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    #timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    #Hour, Minute, Second = timeStamp.split(":")
    #fileName = r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    #with open(r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\Attendance\Attendance.csv", 'a+') as csvFile:
     #       writer = csv.writer(csvFile)
     #       writer.writerow(row)
        #attendance.to_csv(csvFile, index=False)
    print("Attendance Successful")
    cam.release()
    cv2.destroyAllWindows()


