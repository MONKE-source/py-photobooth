import cv2
import numpy as np
import mediapipe as mp
import time

# Face Mesh Detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


def photobooth(chosen_prop, prop_type):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Load the prop image with an alpha channel (transparency)
    image = cv2.imread(chosen_prop, cv2.IMREAD_UNCHANGED)

    with mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as face_mesh:
        while cap.isOpened():
            ret, frame = cap.read()

            start = time.time()

            # Resize the frame to reduce processing time
            frame = cv2.resize(frame, (854, 480))

            frame.flags.writeable = False

            # Process the frame with MediaPipe Face Mesh
            results = face_mesh.process(frame)
            frame.flags.writeable = True

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec,
                    )

                    # Convert face_landmarks to NumPy array for easier indexing
                    landmarks = np.array(
                        [
                            (lm.x * frame.shape[1], lm.y * frame.shape[0])
                            for lm in face_landmarks.landmark
                        ]
                    )

                    left_eye, right_eye, nose_bridge = None, None, None
                    left_cheek, right_cheek = None, None
                    mouth_left, mouth_right, mouth_bottom = None, None, None

                    if prop_type == "glasses":
                        left_eye = landmarks[33]
                        right_eye = landmarks[263]
                        nose_bridge = landmarks[6]
                    elif prop_type == "masks":
                        left_eye = landmarks[33]
                        right_eye = landmarks[263]
                        left_cheek = landmarks[234]
                        right_cheek = landmarks[454]
                        nose_bridge = landmarks[6]
                    elif prop_type == "speech":
                        mouth_left = landmarks[61]
                        mouth_right = landmarks[291]
                        mouth_bottom = landmarks[17]

                    # Draw circles on specific landmarks if they are defined
                    if (
                        left_eye is not None
                        and right_eye is not None
                        and nose_bridge is not None
                    ):
                        cv2.circle(
                            frame,
                            (int(left_eye[0]), int(left_eye[1])),
                            2,
                            (0, 255, 0),
                            -1,
                        )
                        cv2.circle(
                            frame,
                            (int(right_eye[0]), int(right_eye[1])),
                            2,
                            (0, 0, 255),
                            -1,
                        )
                        cv2.circle(
                            frame,
                            (int(nose_bridge[0]), int(nose_bridge[1])),
                            2,
                            (255, 0, 0),
                            -1,
                        )

                    if (
                        prop_type == "masks"
                        and left_cheek is not None
                        and right_cheek is not None
                    ):
                        cv2.circle(
                            frame,
                            (int(left_cheek[0]), int(left_cheek[1])),
                            2,
                            (255, 255, 0),
                            -1,
                        )
                        cv2.circle(
                            frame,
                            (int(right_cheek[0]), int(right_cheek[1])),
                            2,
                            (255, 0, 255),
                            -1,
                        )

                    if (
                        prop_type == "speech"
                        and mouth_left is not None
                        and mouth_right is not None
                        and mouth_bottom is not None
                    ):
                        cv2.circle(
                            frame,
                            (int(mouth_left[0]), int(mouth_left[1])),
                            2,
                            (0, 255, 255),
                            -1,
                        )
                        cv2.circle(
                            frame,
                            (int(mouth_right[0]), int(mouth_right[1])),
                            2,
                            (255, 255, 0),
                            -1,
                        )
                        cv2.circle(
                            frame,
                            (int(mouth_bottom[0]), int(mouth_bottom[1])),
                            2,
                            (255, 0, 255),
                            -1,
                        )

                    # Calculate position of the prop
                    if (
                        prop_type == "glasses"
                        and left_eye is not None
                        and right_eye is not None
                    ):
                        eye_distance = np.linalg.norm(left_eye - right_eye)
                        prop_width = int(eye_distance * 1.5)
                        prop_height = int(
                            prop_width * (image.shape[0] / image.shape[1])
                        )
                    elif (
                        prop_type == "masks"
                        and left_cheek is not None
                        and right_cheek is not None
                    ):
                        cheek_distance = np.linalg.norm(left_cheek - right_cheek)
                        prop_width = int(cheek_distance * 1.2)
                        prop_height = int(
                            prop_width * (image.shape[0] / image.shape[1])
                        )
                    elif (
                        prop_type == "speech"
                        and mouth_left is not None
                        and mouth_right is not None
                    ):
                        mouth_width = np.linalg.norm(mouth_left - mouth_right)
                        prop_width = int(mouth_width * 2)
                        prop_height = int(
                            prop_width * (image.shape[0] / image.shape[1])
                        )

                    if prop_type in ["glasses", "masks", "speech"]:
                        # resize prop
                        prop_resized = cv2.resize(image, (prop_width, prop_height))

                        # Calculate the center of the prop
                        prop_center = (prop_width // 2, prop_height // 2)

                        # Calculate the angle between left and right in radians
                        if prop_type == "glasses" or prop_type == "masks":
                            angle_radians = -1 * np.arctan2(
                                right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]
                            )
                        elif prop_type == "speech":
                            angle_radians = 0

                        # Convert to degrees
                        angle_degrees = np.degrees(angle_radians)

                        # rotate prop properly
                        M = cv2.getRotationMatrix2D(prop_center, angle_degrees, 1)
                        rotated_overlay = cv2.warpAffine(
                            prop_resized,
                            M,
                            (prop_width, prop_height),
                            flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT,
                            borderValue=(0, 0, 0, 0),
                        )

                        # calculate center position
                        if prop_type == "glasses":
                            x_offset = int(nose_bridge[0] - prop_width / 2)
                            y_offset = int(nose_bridge[1] - prop_height / 2)
                        elif prop_type == "masks":
                            x_offset = int(nose_bridge[0] - prop_width / 2)
                            y_offset = int(nose_bridge[1] - prop_height / 1.9)
                        elif prop_type == "speech":
                            x_offset = int(mouth_right[0] - prop_width / 2 + 40)
                            y_offset = int(mouth_bottom[1] - prop_height / 2 - 40)

                        # ensure overlay within proper bounds
                        y1, y2 = max(0, y_offset), min(
                            frame.shape[0], y_offset + prop_height
                        )
                        x1, x2 = max(0, x_offset), min(
                            frame.shape[1], x_offset + prop_width
                        )

                        # Adjust the overlay region if it goes out of bounds
                        overlay_y1 = max(0, -y_offset)
                        overlay_y2 = prop_height - max(
                            0, (y_offset + prop_height) - frame.shape[0]
                        )
                        overlay_x1 = max(0, -x_offset)
                        overlay_x2 = prop_width - max(
                            0, (x_offset + prop_width) - frame.shape[1]
                        )

                        # Calculate the regions of interest
                        overlay_roi = rotated_overlay[
                            overlay_y1:overlay_y2, overlay_x1:overlay_x2
                        ]
                        frame_roi = frame[y1:y2, x1:x2]

                        # Ensure the shapes match before blending
                        if overlay_roi.shape[:2] == frame_roi.shape[:2]:
                            alpha_channel = overlay_roi[:, :, 3] / 255.0
                            alpha_frame = 1.0 - alpha_channel
                            frame_roi[:, :, :3] = (
                                alpha_channel[..., None] * overlay_roi[:, :, :3]
                                + alpha_frame[..., None] * frame_roi[:, :, :3]
                            )
                            frame[y1:y2, x1:x2] = frame_roi

            # display the frames per second
            end = time.time()
            fps = 1 / (end - start)
            cv2.putText(
                frame,
                f"FPS: {fps:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            # Display the frame with the overlay
            cv2.imshow("Prop Filter", frame)

            # to break press q
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # close the camera
    cap.release()
    cv2.destroyAllWindows()
