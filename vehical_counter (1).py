import cv2
import time
import numpy as np
from datetime import date
from datetime import datetime
import math

#line number = 12 13 96 97
endCoordinates = [(5, 597), (337, 343), (772, 344), (1157, 709)]
counterLine = [(337, 343), (772, 344)]
dist=((counterLine[1][0]-counterLine[0][0]) + (counterLine[1][1]-counterLine[0][1]))**0.5
dist=math.floor(dist)

cap=cv2.VideoCapture('video.mp4')

algo=cv2.createBackgroundSubtractorMOG2()

count_line_position=550
min_width_react=80
min_height_react=80

def center_handle(x,y,w,h):
  x1=int(w/2)
  y1=int(h/2)
  cx=x+x1
  cy=y+y1
  return cx,cy

detect=[]
offset=6
counter=0

flag=True

dur = 10
start = time.time()
g_time = 5
v_cnt = True

while flag:
    ret,frame1 = cap.read()
    swtime = "{:02d}".format(dur-int(time.time()-start))


    grey=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(grey,(3,3),3)
    img_sub=algo.apply(blur)
    dilat=cv2.dilate(img_sub,np.ones((5,5)))
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada=cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
    dilatada=cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)
    counterShape,_=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1,counterLine[0],counterLine[1],(255,255,255),3)

    cv2.line(frame1, endCoordinates[0], endCoordinates[1], (0,255,0), 3, cv2.LINE_AA)
    cv2.line(frame1, endCoordinates[2], endCoordinates[3], (0,255,0), 3, cv2.LINE_AA)


    for (i,c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_react) and (h>=min_height_react)
        if not validate_counter:
            continue
        # cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)

        center=center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,0,255),-1)

        for (x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter+=1
                cv2.line(frame1,counterLine[0],counterLine[1],(0,127,255),3)

                detect.remove((x,y))

    today = date.today()
    now = datetime.now()
    cv2.putText(frame1, now.strftime("%H:%M:%S"), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(frame1, today.strftime("%d-%m-%y"), (90,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
    cv2.rectangle(frame1,(70,72),(90,210),(0,0,0),50, cv2.LINE_AA)

    cv2.putText(frame1,"VEHICLE COUNTER : "+str(counter),(900,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 2, cv2.LINE_AA)

    if(time.time()<=start+dur-3):
        cv2.circle(frame1,(80,80),10,(0,0,255),30, cv2.LINE_AA)
        cv2.putText(frame1, swtime, (60,89), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
    elif(time.time()>start+dur-3 and time.time()<=start+dur):
        cv2.circle(frame1,(80,140),10,(0,255,255),30, cv2.LINE_AA)
        cv2.putText(frame1, swtime, (60,149), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        if(v_cnt==True):
            print("Total vehical : ",counter)
            n=(counter*5.2)/dist
            timer=((counter*5.2)/dist)*n
            print(math.ceil(timer))
            v_cnt=False
    else:
        v_cnt=True
        counter=0

        cv2.circle(frame1,(80,200),10,(0,255,0),30, cv2.LINE_AA)
        cv2.putText(frame1, "{:02d}".format(int(swtime)+g_time), (60,209), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        if(int(swtime)+g_time<=0):
            start=time.time() #receive another red signal input

    cv2.imshow('Video original',frame1)
    
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()
cap.release()



# cap = np.zeros([512,512,3], np.uint8)
# vid=cv2.VideoCapture('video.mp4')
# start=time.time()
# flags = True
# while(True):
#     ret, cap=vid.read()
#     realt = time.time()
#     btime=2
    # if(int(realt)%2==0):
    #     cv2.circle(cap,(80,200),10,(0,255,0),30, cv2.LINE_AA) #green
#     cv2.imshow('blinks', cap)
#     if(cv2.waitKey(1)==ord('q')):
#         cv2.destroyAllWindows()
#         break



# import cv2
# import time
# import numpy as np
# from datetime import date
# from datetime import datetime

# endCoordinates = [(5, 597), (337, 343), (772, 344), (1157, 709)]
# counterLine = [(337, 343), (772, 344)]

# cap=cv2.VideoCapture('video.mp4')

# algo=cv2.createBackgroundSubtractorMOG2()

# count_line_position=550
# min_width_react=80
# min_height_react=80

# def center_handle(x,y,w,h):
#   x1=int(w/2)
#   y1=int(h/2)
#   cx=x+x1
#   cy=y+y1
#   return cx,cy

# detect=[]
# offset=6
# counter=0
# flag=True


# start = time.localtime().tm_sec
# dur = 10

# wig = True
# redi = True

# while flag:
#     ret,frame1 = cap.read()
#     realt = time.time()
#     grey=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
#     blur=cv2.GaussianBlur(grey,(3,3),3)
#     img_sub=algo.apply(blur)
#     dilat=cv2.dilate(img_sub,np.ones((5,5)))
#     kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
#     dilatada=cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
#     dilatada=cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)
#     counterShape,_=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#     cv2.line(frame1,counterLine[0],counterLine[1],(255,255,255),3)

#     cv2.line(frame1, endCoordinates[0], endCoordinates[1], (0,255,0), 3, cv2.LINE_AA)
#     cv2.line(frame1, endCoordinates[2], endCoordinates[3], (0,255,0), 3, cv2.LINE_AA)


#     for (i,c) in enumerate(counterShape):
#         (x,y,w,h) = cv2.boundingRect(c)
#         validate_counter = (w>=min_width_react) and (h>=min_height_react)
#         if not validate_counter:
#             continue
#         # cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)

#         center=center_handle(x,y,w,h)
#         detect.append(center)
#         cv2.circle(frame1,center,4,(0,0,255),-1)

#         for (x,y) in detect:
#             if y<(count_line_position+offset) and y>(count_line_position-offset):
#                 counter+=1
#                 cv2.line(frame1,counterLine[0],counterLine[1],(0,127,255),3)

#                 detect.remove((x,y))
#                 # print("VEHICLE COUNTER "+str(counter))

#     today = date.today()
#     now = datetime.now()
#     cv2.putText(frame1,"VEHICLE COUNTER : "+str(counter),(900,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 2, cv2.LINE_AA)
#     cv2.putText(frame1, now.strftime("%H:%M:%S"), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
#     cv2.putText(frame1, today.strftime("%d-%m-%y"), (90,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
#     cv2.rectangle(frame1,(70,72),(90,210),(0,0,0),50, cv2.LINE_AA)

#     if(time.localtime().tm_sec>=start+dur-2 and time.localtime().tm_sec<start+dur):
#         cv2.circle(frame1,(80,140),10,(0,255,255),30, cv2.LINE_AA)
#         if(counter!=0 and wig==True):
#             print("Total vehicle : ",counter)
#             counter=0
#             wig=False
#     elif(time.localtime().tm_sec>=start+dur):
#         if(int(realt)%2==0):
#             cv2.circle(frame1,(80,200),10,(0,255,0),30, cv2.LINE_AA)
#             counter=0
#     else:
#         cv2.circle(frame1,(80,80),10,(0,0,255),30, cv2.LINE_AA)
#         # cv2.putText(frame1,"VEHICLE COUNTER : "+str(counter),(900,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 2, cv2.LINE_AA)
#         wig=True
#     cv2.imshow('Video original',frame1)
    
#     if cv2.waitKey(1)==ord('q'):
#         break

# cv2.destroyAllWindows()
# cap.release()



# # cap = np.zeros([512,512,3], np.uint8)
# # vid=cv2.VideoCapture('video.mp4')
# # start=time.time()
# # flags = True
# # while(True):
# #     ret, cap=vid.read()
# #     realt = time.time()
# #     btime=2
#     # if(int(realt)%2==0):
#     #     cv2.circle(cap,(80,200),10,(0,255,0),30, cv2.LINE_AA) #green
# #     cv2.imshow('blinks', cap)
# #     if(cv2.waitKey(1)==ord('q')):
# #         cv2.destroyAllWindows()
# #         break
