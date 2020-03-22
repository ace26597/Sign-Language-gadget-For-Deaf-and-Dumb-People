from Tkinter import *     # for Gui
from PIL import Image     # python imaging library
from PIL import ImageTk
import cv2       #opencv
import time         # delay
import os       
import picamera   # for picamera
from gtts import gTTS      # 
import numpy as np          
import math

root = Tk()
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)

frame1.pack(side=TOP)
frame2.pack(side=LEFT)
frame3.pack(side=LEFT)

im =Image.open('sample.jpg')
im = ImageTk.PhotoImage(im)
#--------------------------------------fUNCTION DEFINATIONS----------------------------------------------- 

def gesture_recognition():
        import picamera
        camera=picamera.PiCamera()
        camera.resolution=(200,200)
        camera.start_preview()
        time.sleep(5)
        camera.capture('image.jpg')
        camera.stop_preview()
        camera.close()

        frame = cv2.imread("image.jpg")
        kernel = np.ones((3,3),np.uint8)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of skin color in HSV
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
        
         #extract skin colur imagw  
        mask1 = cv2.inRange(hsv, lower_skin, upper_skin)

        #extrapolate the hand to fill dark spots within
        mask = cv2.dilate(mask1,kernel,iterations = 4)
        
        #blur the image
        mask = cv2.GaussianBlur(mask,(5,5),100) 
        
        #find contours
        _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
        #find contour of max area(hand)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        
        #approx the contour a little
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
       
        
        #make convex hull around hand
        hull = cv2.convexHull(cnt)
        
        #define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
      
        #find the percentage of area not covered by hand in convex hull
        arearatio=((areahull-areacnt)/areacnt)*100
        print(arearatio)
        #find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        
        # l = no. of defects
        l=0
        
        #code for finding no. of defects due to fingers
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt= (100,180)
            
            
            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
            #distance between point and convex hull
            d=(2*ar)/a
            
            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
        
            # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
            if angle <= 90 and d>30:
                l += 1
                cv2.circle(frame, far, 3, [255,0,0], -1)       
            
        l+=1
        
        #print corresponding gestures which are in their ranges
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l==1:
            if areacnt<2000:
                cv2.putText(frame,'Put hand in the box',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
                 
            else:
                if arearatio<12:
                    cv2.putText(frame,'No',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
                    print("Converting your text to sound . . .")
                    tts = gTTS(text="no please....", lang='en')
                    tts.save("voice.mp3")
                    print("Starting audio. . .")
                    os.system('omxplayer -o local voice.mp3')
 
                elif arearatio<13.5:
                    cv2.putText(frame,'Best of luck',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
                    print("Converting your text to sound . . .")
                    tts = gTTS(text="Best of luck ...", lang='en')
                    tts.save("voice.mp3")
                    print("Starting audio. . .")
                    os.system('omxplayer -o local voice.mp3')
                    
                else:
                    cv2.putText(frame,'Hello !',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
                    print("Converting your text to sound . . .")
                    tts = gTTS(text="hey hello ...", lang='en')
                    tts.save("voice.mp3")
                    print("Starting audio. . .")
                    os.system('omxplayer -o local voice.mp3')
                
                    
        elif l==2:
            cv2.putText(frame,'please help me',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            print("Converting your text to sound . . .")
            tts = gTTS(text="please help me", lang='en')
            tts.save("voice.mp3")
            print("Starting audio. . .")
            os.system('omxplayer -o local voice.mp3')
            
        elif l==3:
         
              if arearatio<27:
                    cv2.putText(frame,'I am thirsty.',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
                    print("Converting your text to sound . . .")
                    tts = gTTS(text="I am thirsty........", lang='en')
                    tts.save("voice.mp3")
                    print("Starting audio. . .")
                    os.system('omxplayer -o local voice.mp3')

              else:
                    cv2.putText(frame,'ok',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
                    print("Converting your text to sound . . .")
                    tts = gTTS(text="ok .", lang='en')
                    tts.save("voice.mp3")
                    print("Starting audio. . .")
                    os.system('omxplayer -o local voice.mp3')
                    
        elif l==4:
            cv2.putText(frame,'i want tea',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            print("Converting your text to sound . . .")
            tts = gTTS(text="i want tea...", lang='en')
            tts.save("voice.mp3")
            print("Starting audio. . .")
            os.system('omxplayer -o local voice.mp3')
            
        elif l==5:
            cv2.putText(frame,'Thank you !',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            print("Converting your text to sound . . .")
            tts = gTTS(text="Thank you!", lang='en')
            tts.save("voice.mp3")
            print("Starting audio. . .")
            os.system('omxplayer -o local voice.mp3')
            
        elif l==6:
            cv2.putText(frame,'reposition',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            
        else :
            cv2.putText(frame,'reposition',(10,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
             
        cv2.imwrite("frame.jpg", frame)
        im1 = Image.open("frame.jpg")
        im1 = ImageTk.PhotoImage(im1)
        photo1.config(image = im1)
        photo1.image=im1
        
        cv2.imwrite("mask.jpg", mask1)
        im2 = Image.open("mask.jpg")
        im2 = ImageTk.PhotoImage(im2)
        photo2.config(image = im2)
        photo2.image=im2

title = Label(frame1,text = 'Hand gesture Recognition',font = 30,width=50,height=5).pack()

photo1 = Label(frame3,image=im,width=400,height=400,bg='white')
photo1.grid(row=0,column=0,padx=10,pady=10)

result1 = Label(frame3,text= 'Captured Frame',font = 20,width=35,height=3)
result1.grid(row=1,column=0,padx=10,pady=10)

photo2 = Label(frame3,image=im,width=400,height=400,bg='white')
photo2.grid(row=0,column=1,padx=10,pady=10)

result2 = Label(frame3,text= 'Extracted skin colour image',font = 20,width=35,height=3)
result2.grid(row=1,column=1,padx=10,pady=10)


button2 = Button(frame2,font=('courier',10),text = "Gesture Recognition",width=20,height=3,command = gesture_recognition).grid(row=1,column=0,padx=10,pady=10)

root.mainloop()


'''
0 = No
1 = Hello
2 = Please help me
3 = I am Thristy
4 = Yes
5 = Thank you.
'''
