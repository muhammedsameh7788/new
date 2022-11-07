
# this code to run is to import OpenCV
import cv2
import csv
import time
from time import sleep
#adding time and date stuff and rearranging it
from datetime import date, datetime
import random
import RPi.GPIO as IO


ir1 = 21
ir2 = 20

IO.setmode(IO.BCM)
IO.setup(ir1,IO.IN)
IO.setup(ir2,IO.IN)

speed = 0
c = 200
direction = "null"
state = 0

flag_for = False
flag_back = False
flag = False

'''start = 0
end = 0
time = 0
timeRN = 0
date = 0
'''
#data of car one
name_one = "ahmed omar"
number_one = "hfs 123"

#data of car two
name_two = "alla ahmed"
number_two = "kas 834"

#data of car three
name_three = "karim noor"
number_three = "lds 001"


today = date.today()
date = today.strftime("%d-%b-%Y")

# set up camera object called Cap which we will use to find OpenCV
cap = cv2.VideoCapture(0)

# QR code detection Method
detector = cv2.QRCodeDetector()

#This creates an Infinite loop to keep your camera searching for data at all times
while True:
    
    # Below is the method to get a image of the QR code
    _, img = cap.read()
    
    # Below is the method to read the QR code by detetecting the bounding box coords and decoding the hidden QR data 
    data, bbox, _ = detector.detectAndDecode(img)
    
    # This is how we get that Blue Box around our Data. This will draw one, and then Write the Data along with the top
    if(bbox is not None):
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                     0, 0), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 250, 120), 2)
        
        #Below prints the found data to the below terminal (This we can easily expand on to capture the data to an Excel Sheet)

        #You can also add content to before the pass. Say the system reads red it'll activate a Red LED and the same for Green.
        if data and IO.input(ir1) == False and flag_for == False:
            if flag_back == True:
                now = datetime.now()
                timeRN = now.strftime("%H:%M:%S")
                # time = end - start
                # speed = c / time
                speed = random.randint(25,95)
                if spped > 60:
                    state = "over spped"
                else:
                    state = "normal"
                print("data found: ", data, date,timeRN,speed)
                flag_back = False
                
                if data == "OPT":
                    with open('Database.csv', mode='a') as csvfile:
                        csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csvfileWriter.writerow([data, date,timeRN, name_one,number_one,direction,speed,state])
                elif data == "ZXJ":
                    with open('Database.csv', mode='a') as csvfile:
                        csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csvfileWriter.writerow([data, date,timeRN, name_two,number_two,direction,speed,state])
                elif data == "REQ":
                    with open('Database.csv', mode='a') as csvfile:
                        csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csvfileWriter.writerow([data, date,timeRN, name_three,number_three,direction,speed,state])

#del today, date,now, timeRN        
                speed = 0
                direction = "null"
                sleep(5)
            
            else:
                
                flag_for = True
                direction = "forward"
                print("dn")
                
        elif data and IO.input(ir2) == False and flag_back == False:
            if flag_for == True:
                # '''end = time.time()'''
                now = datetime.now()
                timeRN = now.strftime("%H:%M:%S")
                # time = end - start
                # speed = c / time
                speed = random.randint(25,95)
                if spped > 60:
                    state = "over spped"
                else:
                    state = "normal"

                print("data found: ", data, date,timeRN,speed)
                flag_for = False
                
                if data == "ZXJ":
                    with open('Database.csv', mode='a') as csvfile:
                        csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csvfileWriter.writerow([data, date,timeRN, name_two,number_two,direction,speed,state])        
                elif data == "OPT":
                    with open('Database.csv', mode='a') as csvfile:
                        csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csvfileWriter.writerow([data, date,timeRN, name_one,number_one,direction,speed,state])        
                elif data == "REQ":
                    with open('Database.csv', mode='a') as csvfile:
                        csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csvfileWriter.writerow([data, date,timeRN, name_three,number_three,direction,speed,state])        

#del todayx, datex,nowx, timeRNx    
                speed = 0
                direction = "null"
                sleep(5)
                
            else:
               
                flag_back = True
                direction = "backward"
                print("dn")
            
    # Below will display the live camera feed to the Desktop on Raspberry Pi OS preview
    cv2.imshow("code detector", img)
    
    #At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
    if(cv2.waitKey(1) == ord("q")):
        break
    
# When the code is stopped the below closes all the applications/windows that the above has created
cap.release()
cv2.destroyAllWindows()
