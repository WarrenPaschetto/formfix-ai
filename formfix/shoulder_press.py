class ShoulderPressAnalyzer:
    def __init__(self):
        self.rep_count = 0
        self.position = "unknown"

        # These are starting values. We will tune them after testing.
        self.bottom_angle_threshold = 115
        self.top_angle_threshold = 155
        
        # If left and right elbows differ by more than this,
        # we will warn the user.
        self.symmetry_threshold = 20

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
        elbow_difference = abs(left_elbow_angle - right_elbow_angle)

        feedback_messages = []
        
        # Check for uneven arm position
        if elbow_difference > self.symmetry_threshold:
            feedback_messages.append("Even out your arms")

        # Detect bottom position
        if average_elbow_angle < self.bottom_angle_threshold:
            self.position = "bottom"
            feedback_messages.append("Bottom position")

        # Detect completed rep
        elif (
            average_elbow_angle > self.top_angle_threshold
            and self.position == "bottom"
        ):
            self.rep_count += 1
            self.position = "top"
            feedback_messages.append("Rep counted")
            feedback_messages.append("Good lockout")
            
        # Detect top position without counting another rep
        elif average_elbow_angle > self.top_angle_threshold:
            self.position = "top"
            feedback_messages.append("Top position")
            
        # User is somewhere between top and bottom
        else:
            feedback_messages.append("Keep pressing")
        
        # Check lockout quality at the top
        if self.position == "top" and average_elbow_angle < 165:
            feedback_messages.append("Press to full lockout")

        return {
            "rep_count": self.rep_count,
            "position": self.position,
            "average_elbow_angle": average_elbow_angle,
            "elbow_difference": elbow_difference,
            "feedback": " | ".join(feedback_messages),
        }