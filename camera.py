import cv2
import dlib
import numpy as np

# Load the pre-trained face detector and landmark predictor
face_detector = dlib.get_frontal_face_detector()
try:
    landmark_predictor = dlib.shape_predictor(
        "models/shape_predictor_68_face_landmarks.dat"
    )
except RuntimeError as e:
    print(f"Error loading landmark predictor: {e}")
    exit()


def photobooth_glasses(chosen_prop):
    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Resize the frame to reduce processing time
        frame = cv2.resize(frame, (854, 480))

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_detector(gray)

        for face in faces:
            # Detect facial landmarks
            landmarks = landmark_predictor(gray, face)

            # Convert landmarks to NumPy array for easier indexing
            landmarks = np.array(
                [(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)]
            )

            # 2D image points
            image_points = np.array(
                [
                    (landmarks[30][0], landmarks[30][1]),  # Nose tip
                    (landmarks[8][0], landmarks[8][1]),  # Chin
                    (landmarks[36][0], landmarks[36][1]),  # Left eye left corner
                    (landmarks[45][0], landmarks[45][1]),  # Right eye right corner
                    (landmarks[48][0], landmarks[48][1]),  # Left Mouth corner
                    (landmarks[54][0], landmarks[54][1]),  # Right Mouth corner
                ],
                dtype=np.float64,
            )

            # Load the glasses image with an alpha channel (transparency)
            image = cv2.imread(chosen_prop, cv2.IMREAD_UNCHANGED)
            if image is None:
                print(f"Error: Could not load image {chosen_prop}")
                continue

            # Calculate the position of the glasses
            glasses_width = int(np.linalg.norm(landmarks[36] - landmarks[45]) * 1.5)
            glasses_height = int(glasses_width * (image.shape[0] / image.shape[1]))

            # Resize the glasses image to match the calculated size
            glasses_resized = cv2.resize(image, (glasses_width, glasses_height))

            # Calculate the angle between landmarks[36] and landmarks[45] in radians
            angle_radians = -1 * np.arctan2(
                landmarks[45][1] - landmarks[36][1], landmarks[45][0] - landmarks[36][0]
            )

            # Convert the angle from radians to degrees
            angle_degrees = np.degrees(angle_radians)

            # Calculate the center of the glasses
            glasses_center = (glasses_width // 2, glasses_height // 2)

            # Rotate the glasses based on the angle
            M = cv2.getRotationMatrix2D(glasses_center, angle_degrees, 1)
            rotated_overlay = cv2.warpAffine(
                glasses_resized,
                M,
                (glasses_width, glasses_height),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(0, 0, 0, 0),
            )

            if chosen_prop == "props/speech2.png":
                x_offset = int(landmarks[54][0] - glasses_width / 2 + 40)
                y_offset = int(landmarks[54][1] - glasses_height / 2 - 40)
            else:
                x_offset = int(landmarks[27][0] - glasses_width / 2)
                y_offset = int(landmarks[27][1] - glasses_height / 2)

            # Ensure the overlay is within the frame boundaries
            y1, y2 = max(0, y_offset), min(frame.shape[0], y_offset + glasses_height)
            x1, x2 = max(0, x_offset), min(frame.shape[1], x_offset + glasses_width)

            # Adjust the overlay region if it goes out of bounds
            overlay_y1 = max(0, -y_offset)
            overlay_y2 = glasses_height - max(
                0, (y_offset + glasses_height) - frame.shape[0]
            )
            overlay_x1 = max(0, -x_offset)
            overlay_x2 = glasses_width - max(
                0, (x_offset + glasses_width) - frame.shape[1]
            )

            # Calculate the regions of interest
            overlay_roi = rotated_overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
            frame_roi = frame[y1:y2, x1:x2]

            # Ensure the shapes match before blending
            if overlay_roi.shape[:2] == frame_roi.shape[:2]:
                # Calculate the alpha values for blending
                alpha_channel = overlay_roi[:, :, 3] / 255.0
                alpha_frame = 1.0 - alpha_channel

                # Blend the overlay with the frame
                for c in range(3):
                    frame_roi[:, :, c] = (
                        alpha_channel * overlay_roi[:, :, c]
                        + alpha_frame * frame_roi[:, :, c]
                    )

                # Place the blended ROI back onto the frame
                frame[y1:y2, x1:x2] = frame_roi

        # Display the frame with the overlay
        cv2.imshow("Glasses Filter", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()
