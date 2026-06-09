import cv2
import mediapipe as mp


def find_available_cameras(max_index=10):
    available_cameras = []

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


def choose_camera():
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
            print("Please enter a valid number.")


def main():
    camera_index = choose_camera()

    if camera_index is None:
        return

    print(f"\nStarting FormFix AI with camera {camera_index}...")

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

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

            cv2.putText(
                frame,
                f"Camera: {camera_index} | Press q to quit",
                (20, 40),
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