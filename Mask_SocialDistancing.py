import cv2
from scipy.spatial import distance as dist
from tkinter import *
from tkinter import ttk


root = Tk()
root.geometry("500x500")
root.configure(bg='NavajoWhite')
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Click Here to Start the EPS").grid(column=100, row=150)
ttk.Button(frm, text="Start" ,command=root.destroy).grid(column=400, row=400) 
root.mainloop()


cap = cv2.VideoCapture(0)
face_model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_model = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")
mouth_model = cv2.CascadeClassifier('Mouth.xml')


bw_threshold = 80
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 30)
weared_mask_font_color = (0, 255, 0)
not_weared_mask_font_color = (0, 0, 255)
thickness = 2
font_scale = 1
weared_mask = "Thank You for wearing MASK"
not_weared_mask = "PLEASE WEAR MASK"


while True:
    status , photo = cap.read()
    face_cor = face_model.detectMultiScale(photo)
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    faces = face_model.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(photo, (x,y), (x+w,y+h),(255,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = photo[y:y+h, x:x+w]
        mouth_rects = mouth_model.detectMultiScale(gray, 1.5, 5)
        eyes = eye_model.detectMultiScale(roi_gray)
        for(ex,ey,ew,eh) in eyes:
            if(len(mouth_rects) == 0):
                cv2.putText(photo, weared_mask, org , font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        else:
            for (mx, my, mw, mh) in mouth_rects:
                if(y < my < y + h):
                    cv2.putText(photo,not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    break
               
                k = cv2.waitKey(5)
                if k ==27:
                    break


    
    l = len(face_cor)
    photo = cv2.putText(photo, str(len(face_cor))+" Face", (450, 70), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0) , 2, cv2.LINE_AA)
    stack_x = []
    stack_y = []
    stack_x_print = []
    stack_y_print = []
    global D

    if len(face_cor) == 0:
        pass
    else:
        for i in range(0,len(face_cor)):
            x1 = face_cor[i][0]
            y1 = face_cor[i][1]
            x2 = face_cor[i][0] + face_cor[i][2]
            y2 = face_cor[i][1] + face_cor[i][3]

            mid_x = int((x1+x2)/2)
            mid_y = int((y1+y2)/2)
            stack_x.append(mid_x)
            stack_y.append(mid_y)
            stack_x_print.append(mid_x)
            stack_y_print.append(mid_y)

            photo = cv2.circle(photo, (mid_x, mid_y), 3 , [255,0,0] , -1)
           

        if len(face_cor) == 2:
            D = int(dist.euclidean((stack_x.pop(), stack_y.pop()), (stack_x.pop(), stack_y.pop())))
            photo = cv2.line(photo, (stack_x_print.pop(), stack_y_print.pop()), (stack_x_print.pop(), stack_y_print.pop()), [0,0,255], 2)
        else:
            D = 0

        if D<250 and D!=0:
            photo = cv2.putText(photo, " Move Away !!", (100, 150), cv2.FONT_HERSHEY_SIMPLEX,2, [0,0,255] , 3)

        photo = cv2.putText(photo, str(D/10) + " cm", (450, 100), cv2.FONT_HERSHEY_SIMPLEX,
                   1, (255, 0, 0) , 2, cv2.LINE_AA)

        cv2.imshow('video1' , photo)
        if cv2.waitKey(100) == 13:
            break

cv2.destroyAllWindows()




