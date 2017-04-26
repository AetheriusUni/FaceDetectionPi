# Marc Raymond A. Serrano
# marc.serrano@ca.rr.com
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import io
import picamera

# allows conversion to numpy array
stream = io.BytesIO()

# haar cascade which detects faces
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.color_effects = (128,128) #makes it grayscale in video
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320,240))

#allows multiple pictures to be taken and saved without replacing the same picture each time
piccount = 0
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

        #Convert the picture into a numpy array
        buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

        # convert to gray scale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
        # finds faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        
        # Draw a rectangle around every found face
        i = 0;
        for (x,y,w,h) in faces:
            i = i + 1;
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2) #(image, bottom left corner, top right corner, color settings, shift
            cv2.putText(image,"Person",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,255)
            cv2.putText(image,"Number of People = "+str(i),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1,255)
	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
        # if the 'p' key was pressed, take a picture of the current screen and save in current directory (/home/pi in my case)
        if key == ord("p"):
                piccount = piccount + 1
                cv2.imwrite('picture' + str(piccount) +'.jpg',image)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
