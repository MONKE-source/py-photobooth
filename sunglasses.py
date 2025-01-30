# copied from gc
# added comments for my understanding
from imutils import face_utils
import imutils
import dlib
import cv2


p = "models/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

sunglasses = cv2.imread("props/heart2.png")
# cv2.imshow("Test", sunglasses)

cap = cv2.VideoCapture(0)

while True:
    # Getting out image by webcam
    _, image = cap.read()

    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Get faces into webcam's image
    rects = detector(gray, 0)

    # For each detected face, find the landmark.
    for i, rect in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # finds the left and right eye and marks them with colored circles
        left_eye = shape[36]
        right_eye = shape[45]
        bottom_eye = shape[41]
        top_eye = shape[38]
        cv2.circle(image, left_eye, 2, (0, 255, 0), -1)
        cv2.circle(image, right_eye, 2, (0, 0, 255), -1)

        # resizes the sunglasses to fit the persons face
        sun_filter = imutils.resize(sunglasses, width=(right_eye[0] - left_eye[0]))
        # converts to greyscale
        sun_filter_grey = cv2.cvtColor(sun_filter, cv2.COLOR_BGR2GRAY)
        # creates a binary mask which is used to overlay the sunglasses on the persons face
        _, sun_mask = cv2.threshold(sun_filter_grey, 25, 255, cv2.THRESH_BINARY_INV)

        # used to correctly position the glasses on the fella
        sun_height = sun_filter.shape[0]
        sun_width = sun_filter.shape[1]

        # the region of interest
        eye_area = image[
            bottom_eye[1] : bottom_eye[1] + sun_height,
            left_eye[0] : left_eye[0] + sun_width,
        ]

        # applies the mask
        # overlays the sunglasses
        eye_area_no_eyes = cv2.bitwise_and(eye_area, eye_area, mask=sun_mask)
        final_eyes = cv2.add(eye_area_no_eyes, sun_filter)

        # correctly blends the image
        image[
            bottom_eye[1] : bottom_eye[1] + sun_height,
            left_eye[0] : left_eye[0] + sun_width,
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
