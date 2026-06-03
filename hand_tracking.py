import cv2
import mediapipe as mp
import math

class HandTracker:

    def __init__(
        self,
        mode=False,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):

        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )

        self.mp_draw = mp.solutions.drawing_utils

        self.tip_ids = [4, 8, 12, 16, 20]

        self.landmark_list = []

    def detect_hands(self, frame, draw=True):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:

            for hand_landmarks in self.results.multi_hand_landmarks:

                if draw:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

        return frame

    def find_position(self, frame, hand_no=0):

        self.landmark_list = []

        if self.results.multi_hand_landmarks:

            my_hand = self.results.multi_hand_landmarks[hand_no]

            h, w, c = frame.shape

            for idx, lm in enumerate(my_hand.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                self.landmark_list.append(
                    [idx, cx, cy]
                )

        return self.landmark_list

    def fingers_up(self):

        fingers = []

        if len(self.landmark_list) == 0:
            return []

        if self.landmark_list[self.tip_ids[0]][1] > self.landmark_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for i in range(1, 5):

            if self.landmark_list[self.tip_ids[i]][2] < self.landmark_list[self.tip_ids[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def get_distance(self, p1, p2):

        if len(self.landmark_list) == 0:
            return 0

        x1 = self.landmark_list[p1][1]
        y1 = self.landmark_list[p1][2]

        x2 = self.landmark_list[p2][1]
        y2 = self.landmark_list[p2][2]

        length = math.hypot(
            x2 - x1,
            y2 - y1
        )

        return length

    def get_gesture(self):

        fingers = self.fingers_up()

        if len(fingers) == 0:
            return "No Hand"

        if fingers == [0, 1, 0, 0, 0]:
            return "Volume Control"

        if fingers == [0, 1, 1, 0, 0]:
            return "Brightness Control"

        if fingers == [0, 0, 0, 0, 0]:
            return "Mute"

        if fingers == [1, 1, 1, 1, 1]:
            return "Open Palm"

        return "Tracking"