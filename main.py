import cv2

from formfix.angles import calculate_angle
from formfix.pose_detector import PoseDetector
from formfix.shoulder_press import ShoulderPressAnalyzer
from formfix.squat import SquatAnalyzer
from formfix.lunge import LungeAnalyzer
from formfix.voice_feedback import VoiceFeedback


def choose_exercise():
    print("\nChoose exercise:")
    print("[1] Shoulder press")
    print("[2] Squat")
    print("[3] Lunge")

    while True:
        choice = input("\nEnter exercise number: ")

        if choice == "1":
            return "shoulder_press"

        if choice == "2":
            return "squat"
        if choice == "3":
            return "lunge"

        print("Please choose 1, 2, or 3.")

def choose_lead_leg():
    print("\nChoose lead leg for lunge:")
    print("[1] Left leg forward")
    print("[2] Right leg forward")

    while True:
        choice = input("\nEnter lead leg number: ")

        if choice == "1":
            return "left"

        if choice == "2":
            return "right"

        print("Please choose 1 or 2.")

def draw_common_feedback(frame, analysis):
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


def main():
    exercise = choose_exercise()
    lead_leg = None

    if exercise == "lunge":
        lead_leg = choose_lead_leg()

    # Your laptop webcam is camera 2.
    camera_index = 2

    print(f"\nStarting FormFix AI with camera {camera_index}...")
    print(f"Exercise: {exercise}")
    if exercise == "lunge":
        print(f"Lead leg: {lead_leg}")

    pose_detector = PoseDetector()
    mp_pose = pose_detector.mp_pose

    shoulder_press_analyzer = ShoulderPressAnalyzer()
    squat_analyzer = SquatAnalyzer()
    lunge_analyzer = LungeAnalyzer(lead_leg) if exercise == "lunge" else None

    voice_feedback = VoiceFeedback()
    voice_feedback.speak("FormFix AI initialized. Let's get moving!")

    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Could not open selected webcam.")
        pose_detector.close()
        return

    try:
        while True:
            success, frame = cap.read()

            if not success:
                print("Could not read frame from webcam.")
                break

            frame = cv2.flip(frame, 1)

            results = pose_detector.process_frame(frame)

            if results.pose_landmarks:
                pose_detector.draw_landmarks(frame, results)

                image_height, image_width, _ = frame.shape
                landmarks = results.pose_landmarks.landmark

                # Upper-body landmarks for shoulder press.
                right_shoulder = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_SHOULDER,
                    image_width,
                    image_height,
                )

                right_elbow = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_ELBOW,
                    image_width,
                    image_height,
                )

                right_wrist = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_WRIST,
                    image_width,
                    image_height,
                )

                left_shoulder = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.LEFT_SHOULDER,
                    image_width,
                    image_height,
                )

                left_elbow = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.LEFT_ELBOW,
                    image_width,
                    image_height,
                )

                left_wrist = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.LEFT_WRIST,
                    image_width,
                    image_height,
                )

                # Lower-body landmarks for squat.
                right_hip = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_HIP,
                    image_width,
                    image_height,
                )

                right_knee = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_KNEE,
                    image_width,
                    image_height,
                )

                right_ankle = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.RIGHT_ANKLE,
                    image_width,
                    image_height,
                )

                left_hip = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.LEFT_HIP,
                    image_width,
                    image_height,
                )

                left_knee = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.LEFT_KNEE,
                    image_width,
                    image_height,
                )

                left_ankle = pose_detector.get_landmark_point(
                    landmarks,
                    mp_pose.PoseLandmark.LEFT_ANKLE,
                    image_width,
                    image_height,
                )

                if exercise == "shoulder_press":
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
                        left_shoulder,
                        right_shoulder,
                        left_wrist,
                        right_wrist,
                    )

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

                    draw_common_feedback(frame, analysis)

                    cv2.putText(
                        frame,
                        f"Arm difference: {int(analysis['elbow_difference'])}",
                        (20, 280),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )

                    cv2.putText(
                        frame,
                        f"Wrists overhead: {analysis['wrists_overhead']}",
                        (20, 320),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )

                elif exercise == "squat":
                    right_knee_angle = calculate_angle(
                        right_hip,
                        right_knee,
                        right_ankle,
                    )

                    left_knee_angle = calculate_angle(
                        left_hip,
                        left_knee,
                        left_ankle,
                    )

                    analysis = squat_analyzer.analyze(
                        left_knee_angle,
                        right_knee_angle,
                    )

                    voice_feedback.speak(analysis["voice_feedback"])

                    cv2.putText(
                        frame,
                        f"Right knee angle: {int(right_knee_angle)}",
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )

                    cv2.putText(
                        frame,
                        f"Left knee angle: {int(left_knee_angle)}",
                        (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )

                    draw_common_feedback(frame, analysis)

                    cv2.putText(
                        frame,
                        f"Knee difference: {int(analysis['knee_difference'])}",
                        (20, 280),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )
                    
                elif exercise == "lunge":
                    right_knee_angle = calculate_angle(
                        right_hip,
                        right_knee,
                        right_ankle,
                    )

                    left_knee_angle = calculate_angle(                            left_hip,
                        left_knee,
                        left_ankle,
                    )

                    if lead_leg == "left":
                        lead_knee_angle = left_knee_angle
                        rear_knee_angle = right_knee_angle
                    else:
                        lead_knee_angle = right_knee_angle
                        rear_knee_angle = left_knee_angle

                    analysis = lunge_analyzer.analyze(
                        lead_knee_angle,
                        rear_knee_angle,
                    )

                    voice_feedback.speak(analysis["voice_feedback"])

                    cv2.putText(
                        frame,
                        f"Right knee angle: {int(right_knee_angle)}",
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )

                    cv2.putText(
                        frame,
                        f"Left knee angle: {int(left_knee_angle)}",
                        (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                      )

                    draw_common_feedback(frame, analysis)

                    cv2.putText(
                        frame,
                        f"Lead leg: {analysis['lead_leg']}",
                        (20, 280),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )

                    cv2.putText(
                        frame,
                        f"Rear knee angle: {int(analysis['rear_knee_angle'])}",
                        (20, 320),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2,
                    )

            cv2.putText(
                frame,
                "Press q to quit",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.imshow("FormFix AI - Pose Test", frame)

            key = cv2.waitKey(10) & 0xFF

            if key == ord("q") or key == 27:  # 27 is ESC
                print("Exiting FormFix AI...")
                break
            
    finally:
        pose_detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()