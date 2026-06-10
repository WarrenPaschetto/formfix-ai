class ShoulderPressAnalyzer:
    def __init__(self):
        self.rep_count = 0
        self.position = "unknown"

        # Movement thresholds
        self.bottom_angle_threshold = 115
        self.top_angle_threshold = 155
        self.lockout_angle_threshold = 165
        self.symmetry_threshold = 20

        # Voice event memory
        self.last_voice_event = None

    def analyze(self, left_elbow_angle, right_elbow_angle):
        average_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2
        elbow_difference = abs(left_elbow_angle - right_elbow_angle)

        visual_feedback_messages = []
        voice_feedback = ""

        # Decide the current coaching event.
        current_event = None

        # Priority 1: uneven arms
        if elbow_difference > self.symmetry_threshold:
            visual_feedback_messages.append("Even out your arms")
            current_event = "uneven_arms"

        # Priority 2: bottom position
        if average_elbow_angle < self.bottom_angle_threshold:
            self.position = "bottom"
            visual_feedback_messages.append("Bottom position")

            if current_event is None:
                current_event = "bottom"

        # Priority 3: completed rep
        elif (
            average_elbow_angle > self.top_angle_threshold
            and self.position == "bottom"
        ):
            self.rep_count += 1
            self.position = "top"
            visual_feedback_messages.append("Rep counted")

            current_event = "good_rep"

        # Priority 4: top position
        elif average_elbow_angle > self.top_angle_threshold:
            self.position = "top"
            visual_feedback_messages.append("Top position")

            if average_elbow_angle < self.lockout_angle_threshold:
                visual_feedback_messages.append("Press to full lockout")

                if current_event is None:
                    current_event = "short_lockout"
            else:
                visual_feedback_messages.append("Good lockout")

                if current_event is None:
                    current_event = "good_lockout"

        # Priority 5: middle
        else:
            visual_feedback_messages.append("Keep pressing")

            if current_event is None:
                current_event = "middle"

        # Convert event into a spoken cue.
        if current_event != self.last_voice_event:
            voice_feedback = self._voice_message_for_event(current_event)
            self.last_voice_event = current_event

        visual_feedback = " | ".join(visual_feedback_messages)

        return {
            "rep_count": self.rep_count,
            "position": self.position,
            "average_elbow_angle": average_elbow_angle,
            "elbow_difference": elbow_difference,
            "visual_feedback": visual_feedback,
            "voice_feedback": voice_feedback,
        }

    def _voice_message_for_event(self, event):
        messages = {
            "uneven_arms": "Even out your arms",
            "bottom": "Drive overhead",
            "good_rep": "Good rep",
            "short_lockout": "Finish the lockout",
            "good_lockout": "Good lockout",
            "middle": "",
        }

        return messages.get(event, "")