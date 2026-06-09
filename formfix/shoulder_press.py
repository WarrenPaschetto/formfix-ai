class ShoulderPressAnalyzer:
    def __init__(self):
        self.rep_count = 0
        self.position = "unknown"

        # These are starting values. We will tune them after testing.
        self.bottom_angle_threshold = 115
        self.top_angle_threshold = 155

    def analyze(self, left_elbow_angle, right_elbow_angle):
        """
        Analyze shoulder press form using left and right elbow angles.

        Bottom position:
        - both elbows are bent

        Top position:
        - both elbows are extended overhead

        A rep is counted when the user moves from bottom to top.
        """

        average_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2

        feedback = "Keep pressing"

        if average_elbow_angle < self.bottom_angle_threshold:
            self.position = "bottom"
            feedback = "Bottom position"

        elif (
            average_elbow_angle > self.top_angle_threshold
            and self.position == "bottom"
        ):
            self.rep_count += 1
            self.position = "top"
            feedback = "Rep counted"

        elif average_elbow_angle > self.top_angle_threshold:
            self.position = "top"
            feedback = "Top position"

        return {
            "rep_count": self.rep_count,
            "position": self.position,
            "average_elbow_angle": average_elbow_angle,
            "feedback": feedback,
        }