class ShoulderPressAnalyzer:
    def __init__(self):
        self.rep_count = 0
        self.position = "unknown"

        # Movement thresholds
        self.bottom_angle_threshold = 115
        self.top_angle_threshold = 155
        self.lockout_angle_threshold = 165
        self.symmetry_threshold = 20

        # Wrist-height threshold.
        # Smaller y-value means higher on screen.
        self.overhead_margin_pixels = 20

        # Voice event memory
        self.last_voice_event = None

    def analyze(
        self,
        left_elbow_angle,
        right_elbow_angle,
        left_shoulder,
        right_shoulder,
        left_wrist,
        right_wrist,
    ):
        average_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2
        elbow_difference = abs(left_elbow_angle - right_elbow_angle)

        left_shoulder_x, left_shoulder_y = left_shoulder
        right_shoulder_x, right_shoulder_y = right_shoulder
        left_wrist_x, left_wrist_y = left_wrist
        right_wrist_x, right_wrist_y = right_wrist

        average_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
        average_wrist_y = (left_wrist_y + right_wrist_y) / 2

        wrists_overhead = average_wrist_y < average_shoulder_y - self.overhead_margin_pixels
        wrist_height_difference = abs(left_wrist_y - right_wrist_y)

        visual_feedback_messages = []
        voice_feedback = ""

        current_event = None

        # Priority 1: uneven arms by elbow angle or wrist height.
        if (
            elbow_difference > self.symmetry_threshold
            or wrist_height_difference > 40
        ):
            visual_feedback_messages.append("Even out your arms")
            current_event = "uneven_arms"

        # Bottom position.
        if average_elbow_angle < self.bottom_angle_threshold:
            self.position = "bottom"
            visual_feedback_messages.append("Bottom position")

            if current_event is None:
                current_event = "bottom"

        # Completed rep.
        elif (
            average_elbow_angle > self.top_angle_threshold
            and wrists_overhead
            and self.position == "bottom"
        ):
            self.rep_count += 1
            self.position = "top"
            visual_feedback_messages.append("Rep counted")

            current_event = "good_rep"

        # Top-ish position but not truly overhead.
        elif average_elbow_angle > self.top_angle_threshold:
            self.position = "top"

            if not wrists_overhead:
                visual_feedback_messages.append("Press overhead")

                if current_event is None:
                    current_event = "not_overhead"

            elif average_elbow_angle < self.lockout_angle_threshold:
                visual_feedback_messages.append("Finish the lockout")

                if current_event is None:
                    current_event = "short_lockout"

            else:
                visual_feedback_messages.append("Good lockout")

                if current_event is None:
                    current_event = "good_lockout"

        # Middle position.
        else:
            visual_feedback_messages.append("Keep pressing")

            if current_event is None:
                current_event = "middle"

        if current_event != self.last_voice_event:
            voice_feedback = self._voice_message_for_event(current_event)
            self.last_voice_event = current_event

        visual_feedback = " | ".join(visual_feedback_messages)

        return {
            "rep_count": self.rep_count,
            "position": self.position,
            "average_elbow_angle": average_elbow_angle,
            "elbow_difference": elbow_difference,
            "wrist_height_difference": wrist_height_difference,
            "wrists_overhead": wrists_overhead,
            "visual_feedback": visual_feedback,
            "voice_feedback": voice_feedback,
        }

    def _voice_message_for_event(self, event):
        messages = {
            "uneven_arms": "Even out your arms",
            "bottom": "Drive overhead",
            "good_rep": "Good rep",
            "short_lockout": "Finish the lockout",
            "not_overhead": "Press overhead",
            "good_lockout": "Good lockout",
            "middle": "",
        }

        return messages.get(event, "")