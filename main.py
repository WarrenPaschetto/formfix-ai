import cv2
import mediapipe as mp

from formfix.angles import calculate_angle
from formfix.shoulder_press import ShoulderPressAnalyzer
from formfix.voice_feedback import VoiceFeedback

def get_landmark_point(landmarks, landmark_enum, image_width, image_height):
    landmark = landmarks[landmark_enum.value]

    x = int(landmark.x * image_width)
    y = int(landmark.y * image_height)

    return x, y

''' def find_available_cameras(max_index=10):
    available_cameras = [2]

    print("Scanning for available cameras...")

     for index in range(max_index):
        cap = cv2.VideoCapture(index)

        if cap.isOpened():
            success, _ = cap.read()

            if success:
                available_cameras.append(index)
                print(f"[{index}] Camera available")
            else:
                print(f"[{index}] Opens but cannot read frame")

            cap.release()
        else:
            print(f"[{index}] Not available") 

    return available_cameras
'''

''' def choose_camera():
    available_cameras = find_available_cameras()

    if not available_cameras:
        print("No cameras found.")
        return None

    print("\nAvailable cameras:")
    for index in available_cameras:
        print(f"Camera {index}")

    while True:
        choice = input("\nEnter the camera number you want to use: ")

        try:
            camera_index = int(choice)

            if camera_index in available_cameras:
                return camera_index

            print("That camera number is not in the available list.")

        except ValueError:
            print("Please enter a valid number.") '''


def main():
    camera_index = 2 #choose_camera()

    if camera_index is None:
        return

    print(f"\nStarting FormFix AI with camera {camera_index}...")

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    shoulder_press_analyzer = ShoulderPressAnalyzer()
    voice_feedback = VoiceFeedback()

    # Test voice feedback
    voice_feedback.speak("FormFix AI initialized. Let's get moving!")
            
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Could not open selected webcam.")
        return

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        while True:
            success, frame = cap.read()

            if not success:
                print("Could not read frame from webcam.")
                break

            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                )
                
                image_height, image_width, _ = frame.shape
                landmarks = results.pose_landmarks.landmark

                ''' right_hip = get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_HIP,
                    image_width,
                    image_height,
                )

                right_knee = get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_KNEE,
                    image_width,
                    image_height,
                )

                right_ankle = get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_ANKLE,
                    image_width,
                    image_height,
                )

                right_knee_angle = calculate_angle(
                    right_hip,
                    right_knee,
                    right_ankle,
                )

            cv2.putText(
                frame,
                f"Right knee angle: {int(right_knee_angle)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            ) '''
            
            right_shoulder = get_landmark_point(
                landmarks,
                mp_pose.PoseLandmark.RIGHT_SHOULDER,
                image_width,
                image_height,
            )

            right_elbow = get_landmark_point(
                landmarks,
                mp_pose.PoseLandmark.RIGHT_ELBOW,
                image_width,
                image_height,
            )

            right_wrist = get_landmark_point(
                landmarks,
                mp_pose.PoseLandmark.RIGHT_WRIST,
                image_width,
                image_height,
            )

            left_shoulder = get_landmark_point(
                landmarks,
                mp_pose.PoseLandmark.LEFT_SHOULDER,
                image_width,
                image_height,
            )

            left_elbow = get_landmark_point(
                landmarks,
                mp_pose.PoseLandmark.LEFT_ELBOW,
                image_width,
                image_height,
            )

            left_wrist = get_landmark_point(
                landmarks,
                mp_pose.PoseLandmark.LEFT_WRIST,
                image_width,
                image_height,
            )

            right_elbow_angle = calculate_angle(
                right_shoulder,
                right_elbow,
                right_wrist,
            )

            left_elbow_angle = calculate_angle(
                left_shoulder,
                left_elbow,
                left_wrist,
            )
    
            analysis = shoulder_press_analyzer.analyze(
                left_elbow_angle,
                right_elbow_angle,
        )
            
            # Debugging: print(analysis)
            print("VOICE:", analysis["voice_feedback"])   
            voice_feedback.speak(analysis["voice_feedback"])

            cv2.putText(
                frame,
                f"Right elbow angle: {int(right_elbow_angle)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Left elbow angle: {int(left_elbow_angle)}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            
            cv2.putText(
                frame,
                f"Reps: {analysis['rep_count']}",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Position: {analysis['position']}",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                analysis["visual_feedback"],
                (20, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            
            cv2.putText(
                frame,
                f"Arm difference: {int(analysis['elbow_difference'])}",
                (20, 280),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.imshow("FormFix AI - Pose Test", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()