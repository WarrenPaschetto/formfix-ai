class SquatAnalyzer:
    def __init__(self):
        self.rep_count = 0
        self.position = "unknown"

        # Starting thresholds. We will tune these.
        self.bottom_angle_threshold = 115
        self.standing_angle_threshold = 160

        # Checks left/right knee angle difference.
        self.symmetry_threshold = 20

        self.last_voice_event = None

    def analyze(self, left_knee_angle, right_knee_angle):
        average_knee_angle = (left_knee_angle + right_knee_angle) / 2
        knee_difference = abs(left_knee_angle - right_knee_angle)

        visual_feedback_messages = []
        voice_feedback = ""

        current_event = None

        # Uneven squat depth or shifting to one side.
        if knee_difference > self.symmetry_threshold:
            visual_feedback_messages.append("Even out your legs")
            current_event = "uneven_legs"

        # Bottom position.
        if average_knee_angle < self.bottom_angle_threshold:
            self.position = "bottom"
            visual_feedback_messages.append("Bottom position")

            if current_event is None:
                current_event = "bottom"

        # Completed rep: bottom -> standing.
        elif (
            average_knee_angle > self.standing_angle_threshold
            and self.position == "bottom"
        ):
            self.rep_count += 1
            self.position = "standing"
            visual_feedback_messages.append("Rep counted")

            current_event = "good_rep"

        # Standing position.
        elif average_knee_angle > self.standing_angle_threshold:
            self.position = "standing"
            visual_feedback_messages.append("Standing")

            if current_event is None:
                current_event = "standing"

        # Middle of rep.
        else:
            visual_feedback_messages.append("Keep moving")

            if current_event is None:
                current_event = "middle"

        if current_event != self.last_voice_event:
            voice_feedback = self._voice_message_for_event(current_event)
            self.last_voice_event = current_event

        visual_feedback = " | ".join(visual_feedback_messages)

        return {
            "rep_count": self.rep_count,
            "position": self.position,
            "average_knee_angle": average_knee_angle,
            "knee_difference": knee_difference,
            "visual_feedback": visual_feedback,
            "voice_feedback": voice_feedback,
        }

    def _voice_message_for_event(self, event):
        messages = {
            "uneven_legs": "Even out your legs",
            "bottom": "Drive up",
            "good_rep": "Good rep",
            "standing": "",
            "middle": "",
        }

        return messages.get(event, "")