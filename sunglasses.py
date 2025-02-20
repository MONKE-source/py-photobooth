# NOTE: This is OLD version of the project file, use campera.py instead

# copied from gc
# added comments for my understanding
from imutils import face_utils
import imutils
import dlib
import cv2
import numpy as np

p = "models/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

sunglasses = cv2.imread("props/heart2.png")
# cv2.imshow("Test", sunglasses)

cap = cv2.VideoCapture(1)

while True:
    # Getting out image by webcam
    _, image = cap.read()

    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Get faces into webcam's image
    faces = detector(gray, 0)

    # For each detected face, find the landmark.
    for face in faces:
        # Make the prediction and transfom it to numpy array
        landmark = predictor(gray, face)
        landmark = face_utils.shape_to_np(landmark)

        # finds the left and right eye and marks them with colored circles
        left_eye = landmark[36]
        right_eye = landmark[45]
        bottom_eye = landmark[41]
        top_eye = landmark[38]
        cv2.circle(image, left_eye, 2, (0, 255, 0), -1)
        cv2.circle(image, right_eye, 2, (0, 0, 255), -1)

        # Calculate the angle between eyes
        angle = -1 * np.degrees(np.arctan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]))

        # Calculate the center point between the eyes
        center_x = (left_eye[0] + right_eye[0]) // 2
        center_y = (left_eye[1] + right_eye[1]) // 2

        # resizes the sunglasses to fit the persons face
        sun_filter = imutils.resize(sunglasses, width=(right_eye[0] - left_eye[0]))
        
        # Rotate the sunglasses based on the angle between the eyes
        M = cv2.getRotationMatrix2D((sun_filter.shape[1] // 2, sun_filter.shape[0] // 2), angle, 1)
        sun_filter = cv2.warpAffine(sun_filter, M, (sun_filter.shape[1], sun_filter.shape[0]))

        # converts to greyscale
        sun_filter_grey = cv2.cvtColor(sun_filter, cv2.COLOR_BGR2GRAY)
        # creates a binary mask which is used to overlay the sunglasses on the persons face
        _, sun_mask = cv2.threshold(sun_filter_grey, 25, 255, cv2.THRESH_BINARY_INV)

        # used to correctly position the glasses on the fella
        sun_height = sun_filter.shape[0]
        sun_width = sun_filter.shape[1]

        # the region of interest
        eye_area = image[
            center_y - sun_height // 2 : center_y + sun_height // 2,
            center_x - sun_width // 2 : center_x + sun_width // 2,
        ]

        # Ensure the sun_filter has the same size as the region of interest
        sun_filter_resized = cv2.resize(sun_filter, (eye_area.shape[1], eye_area.shape[0]))

        # Ensure the mask has the same size as the region of interest
        sun_mask_resized = cv2.resize(sun_mask, (eye_area.shape[1], eye_area.shape[0]))
        
        # Debug prints to check dimensions
        # print(f"sun_filter shape: {sun_filter.shape}")
        # print(f"sun_mask shape: {sun_mask.shape}")
        # print(f"eye_area shape: {eye_area.shape}")

        # Check if dimensions match before applying the mask
        eye_area_no_eyes = cv2.bitwise_and(eye_area, eye_area, mask=sun_mask_resized)
        final_eyes = cv2.add(eye_area_no_eyes, sun_filter_resized)

        # correctly blends the image
        image[
            center_y - sun_height // 2 : center_y + sun_height // 2,
            center_x - sun_width // 2 : center_x + sun_width // 2,
        ] = final_eyes
            
    """
        # Draw on our image, all the finded cordinate points (x,y) 
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
    """

    # Show the image
    cv2.imshow("Output", image)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
