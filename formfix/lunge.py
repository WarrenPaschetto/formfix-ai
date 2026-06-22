class LungeAnalyzer:
    def __init__(self, lead_leg):
        self.lead_leg = lead_leg  # "left" or "right"
        self.rep_count = 0
        self.position = "unknown"

        # Starting thresholds. We will tune these.
        self.bottom_angle_threshold = 115
        self.standing_angle_threshold = 155

        # Voice event memory
        self.last_voice_event = None

    def analyze(self, lead_knee_angle, rear_knee_angle):
        visual_feedback_messages = []
        voice_feedback = ""

        current_event = None

        # Bottom position: lead knee is bent.
        if lead_knee_angle < self.bottom_angle_threshold:
            self.position = "bottom"
            visual_feedback_messages.append("Bottom position")

            if current_event is None:
                current_event = "bottom"

        # Completed rep: bottom -> standing.
        elif (
            lead_knee_angle > self.standing_angle_threshold
            and self.position == "bottom"
        ):
            self.rep_count += 1
            self.position = "standing"
            visual_feedback_messages.append("Rep counted")

            current_event = "good_rep"

        # Standing position.
        elif lead_knee_angle > self.standing_angle_threshold:
            self.position = "standing"
            visual_feedback_messages.append("Standing")

            if current_event is None:
                current_event = "standing"

        # Middle of rep.
        else:
            visual_feedback_messages.append("Keep moving")

            if current_event is None:
                current_event = "middle"

        # Simple rear-leg cue.
        if self.position == "bottom" and rear_knee_angle > 150:
            visual_feedback_messages.append("Bend your back knee")

            if current_event is None:
                current_event = "bend_back_knee"

        if current_event != self.last_voice_event:
            voice_feedback = self._voice_message_for_event(current_event)
            self.last_voice_event = current_event

        visual_feedback = " | ".join(visual_feedback_messages)

        return {
            "rep_count": self.rep_count,
            "position": self.position,
            "lead_leg": self.lead_leg,
            "lead_knee_angle": lead_knee_angle,
            "rear_knee_angle": rear_knee_angle,
            "visual_feedback": visual_feedback,
            "voice_feedback": voice_feedback,
        }

    def _voice_message_for_event(self, event):
        messages = {
            "bottom": "Drive up",
            "good_rep": "Good rep",
            "standing": "",
            "middle": "",
            "bend_back_knee": "Bend your back knee",
        }

        return messages.get(event, "")