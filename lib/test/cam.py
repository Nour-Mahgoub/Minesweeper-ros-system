import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FPS, 30)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

if not cap.isOpened():
    print("Camera not working")

while True:   
    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('live', grey)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cv2.destroyAllWindows()
cap.release