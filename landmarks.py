# copied from google classroom
# added more comments for my understanding
from imutils import face_utils
import dlib
import cv2

# Load pre-trained model
p = "models/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

# i love arth
# capture video from mac webcame
cap = cv2.VideoCapture(1)

while True:
    # Read a frame from the video provided
    _, image = cap.read()

    # Convert the frame to grayscale
    # converting to grayscale makes it easier for the model to process the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # For each detected face, find the landmarks
    for i, rect in enumerate(rects):
        # Predict the landmarks and convert to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Draw circles on the landmarks
        for x, y in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    # Display the frame with landmarks
    cv2.imshow("Output", image)

    # Exit loop if 'Esc' key is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# Release the webcam and close all windows
cv2.destroyAllWindows()
cap.release()
