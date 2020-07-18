import cv2 as cv

#open the camera of index 0 for primary and if any other,index goes on increasing
#for playing a video change the index to the file name
cap = cv.VideoCapture(0)

#checks if the camera is opened
if not cap.isOpened():
    print("can't open camera")
    exit(1)


while True:
    #capture frame by frame
    ret, frame = cap.read()

    #checks if frame is read
    if not ret:
        print("Frame can't be read")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("Video Capture", gray)

    if cv.waitKey(100) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()