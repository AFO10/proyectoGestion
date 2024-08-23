import cv2
import numpy as np
#import dlib
from scipy.spatial import distance as dist
from keras.models import load_model

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load the pre-trained ANN model
model = load_model('C:/Users/LENOVO/Videos/drowsiness_detection_model.h5')

# Function to calculate Eye Aspect Ratio (EAR)
def calculate_EAR(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    EAR = (A + B) / (2.0 * C)
    return EAR

# Define thresholds
EAR_THRESHOLD = 0.3
CONSEC_FRAMES = 48

# Initialize counters
COUNTER = 0

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye = roi_gray[ey:ey+eh, ex:ex+ew]
            eye = cv2.resize(eye, (24, 24))
            eye = eye.astype('float') / 255.0
            eye = np.expand_dims(eye, axis=0)
            eye = np.expand_dims(eye, axis=3)
            
            # Predict drowsiness
            prediction = model.predict(eye)
            if prediction[0][0] < 0.5:  # Assuming binary classification with 0 for drowsy
                COUNTER += 1
                if COUNTER >= CONSEC_FRAMES:
                    cv2.putText(frame, "PELIGRO!!!!", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                COUNTER = 0
                
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow('Drowsiness Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
