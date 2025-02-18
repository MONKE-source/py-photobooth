import cv2
import dlib
import numpy as np

# Load the pre-trained face detector and landmark predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
		
# Open the webcam
cap = cv2.VideoCapture(1)



while True:
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_detector(gray)

    for face in faces:
        # Detect facial landmarks
        landmarks = landmark_predictor(gray, face)

        # Convert landmarks to NumPy array for easier indexing
        landmarks = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)])

        cv2.circle(frame, landmarks[36], 2, (0, 255, 0), -1)
        cv2.circle(frame, landmarks[45], 2, (0, 0, 255), -1)

        # Load the glasses image with an alpha channel (transparency)
        image = cv2.imread("props/yellow_glasses.png", cv2.IMREAD_UNCHANGED)

        # Calculate the position of the glasses
        glasses_width = int(np.linalg.norm(landmarks[36] - landmarks[45]) * 1.5)
        glasses_height = int(glasses_width * (image.shape[0] / image.shape[1]))

        # Resize the glasses image to match the calculated size
        glasses_resized = cv2.resize(image, (glasses_width, glasses_height))

        # Calculate the angle between landmarks[36] and landmarks[45] in radians
        angle_radians = -1 * np.arctan2(landmarks[45][1] - landmarks[36][1], landmarks[45][0] - landmarks[36][0])

        # Convert the angle from radians to degrees
        angle_degrees = np.degrees(angle_radians)

        # Calculate the center of the glasses
        glasses_center = (glasses_width // 2, glasses_height // 2)

        # Rotate the glasses based on the angle
        M = cv2.getRotationMatrix2D(glasses_center, angle_degrees, 1)
        rotated_overlay = cv2.warpAffine(glasses_resized, M, (glasses_width, glasses_height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))

        # Calculate the position to center the glasses
        x_offset = int(landmarks[27][0] - glasses_width / 2)
        y_offset = int(landmarks[27][1] - glasses_height / 2)

        # Ensure the overlay is within the frame boundaries
        y1, y2 = max(0, y_offset), min(frame.shape[0], y_offset + glasses_height)
        x1, x2 = max(0, x_offset), min(frame.shape[1], x_offset + glasses_width)

        # Calculate the regions of interest
        overlay_roi = rotated_overlay[y1 - y_offset:y2 - y_offset, x1 - x_offset:x2 - x_offset]
        frame_roi = frame[y1:y2, x1:x2]

        # Resize the ROI to match the emotion image size
        overlay_roi = cv2.resize(overlay_roi, (x2 - x1, y2 - y1))

        # Calculate the alpha values for blending
        alpha_channel = rotated_overlay[:, :, 3] / 255.0
        alpha_frame = 1.0 - alpha_channel

        # Blend the overlay with the frame
        for c in range(3):
            frame_roi[:, :, c] = (alpha_channel * overlay_roi[:, :, c] + alpha_frame * frame_roi[:, :, c])

        # Place the blended ROI back onto the frame
        frame[y1:y2, x1:x2] = frame_roi

    # Display the frame with the overlay
    cv2.imshow("Glasses Filter", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()