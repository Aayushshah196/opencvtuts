import cv2 as cv

#opening the camera 
cap = cv.VideoCapture(0)

#declaring the codec and video writer
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output2.avi', fourcc, 20.0, (640,480))

#check if the camera is opened
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Can't read the frame. Exiting!!!")
        break

    frame = cv.flip(frame,2)

    out.write(frame)

    cv.imshow('Saving frame', frame)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()