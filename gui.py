import customtkinter as ctk
import cv2
import time
from PIL import Image, ImageTk

from hand_tracking import HandTracker
from volume_controller import VolumeController
from brightness_controller import BrightnessController
from database import GestureDatabase


class GestureControlGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Powered Gesture Control Platform")
        self.geometry("1700x950")
        self.minsize(1400, 800)

        ctk.set_appearance_mode("dark")

        self.cap = cv2.VideoCapture(0)

        self.tracker = HandTracker()
        self.volume_controller = VolumeController()
        self.brightness_controller = BrightnessController()
        self.database = GestureDatabase()

        self.previous_gesture = ""
        self.p_time = time.time()

        self.create_ui()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing
        )

        self.update_camera()

    def create_ui(self):

        # =========================
        # HEADER
        # =========================

        header = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        header.pack(
            fill="x",
            padx=15,
            pady=10
        )

        title = ctk.CTkLabel(
            header,
            text="AI Powered Gesture Control Platform",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            pady=(15, 0)
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Computer Vision • Human Computer Interaction • Automation",
            font=("Segoe UI", 14)
        )

        subtitle.pack(
            pady=(0, 15)
        )

        # =========================
        # BODY
        # =========================

        body = ctk.CTkFrame(self)

        body.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # CAMERA SECTION

        self.camera_frame = ctk.CTkFrame(
            body,
            corner_radius=15
        )

        self.camera_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text=""
        )

        self.camera_label.pack(
            expand=True
        )

        # RIGHT PANEL

        right_panel = ctk.CTkFrame(
            body,
            width=340,
            corner_radius=15
        )

        right_panel.pack(
            side="right",
            fill="y",
            padx=10,
            pady=10
        )

        # STATUS

        self.status_label = ctk.CTkLabel(
            right_panel,
            text="🟢 Tracking",
            font=("Segoe UI", 20, "bold")
        )

        self.status_label.pack(
            pady=(20, 10)
        )

        # GESTURE

        ctk.CTkLabel(
            right_panel,
            text="Current Gesture",
            font=("Segoe UI", 18, "bold")
        ).pack()

        self.gesture_label = ctk.CTkLabel(
            right_panel,
            text="Waiting...",
            font=("Segoe UI", 24)
        )

        self.gesture_label.pack(
            pady=(5, 20)
        )

        # VOLUME

        ctk.CTkLabel(
            right_panel,
            text="Volume",
            font=("Segoe UI", 18, "bold")
        ).pack()

        self.volume_bar = ctk.CTkProgressBar(
            right_panel
        )

        self.volume_bar.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.volume_percent = ctk.CTkLabel(
            right_panel,
            text="0%"
        )

        self.volume_percent.pack()

        # BRIGHTNESS

        ctk.CTkLabel(
            right_panel,
            text="Brightness",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(20, 0))

        self.brightness_bar = ctk.CTkProgressBar(
            right_panel
        )

        self.brightness_bar.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.brightness_percent = ctk.CTkLabel(
            right_panel,
            text="0%"
        )

        self.brightness_percent.pack()

        # FPS

        self.fps_label = ctk.CTkLabel(
            right_panel,
            text="FPS : 0",
            font=("Segoe UI", 16)
        )

        self.fps_label.pack(
            pady=20
        )

        # LOGS

        ctk.CTkLabel(
            right_panel,
            text="Activity Timeline",
            font=("Segoe UI", 18, "bold")
        ).pack()

        self.logs_box = ctk.CTkTextbox(
            right_panel,
            height=250
        )

        self.logs_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def add_log(self, message):

        self.logs_box.insert(
            "1.0",
            message + "\n"
        )

    def update_camera(self):

        success, frame = self.cap.read()

        if success:

            frame = cv2.flip(frame, 1)

            frame = self.tracker.detect_hands(frame)

            self.tracker.find_position(frame)

            gesture = self.tracker.get_gesture()

            self.gesture_label.configure(
                text=gesture
            )

            # Volume Control

            if gesture == "Volume Control":

                distance = self.tracker.get_distance(
                    4,
                    8
                )

                volume = self.volume_controller.set_volume_from_distance(
                    distance
                )

                self.volume_bar.set(
                    volume / 100
                )

                self.volume_percent.configure(
                    text=f"{volume}%"
                )

            # Brightness Control

            elif gesture == "Brightness Control":

                distance = self.tracker.get_distance(
                    4,
                    12
                )

                brightness = self.brightness_controller.set_brightness_from_distance(
                    distance
                )

                self.brightness_bar.set(
                    brightness / 100
                )

                self.brightness_percent.configure(
                    text=f"{brightness}%"
                )

           # elif gesture == "Mute":

            #    self.volume_controller.mute()

            # Logging

            if gesture != self.previous_gesture:

                self.add_log(gesture)

                self.database.log_action(
                    gesture,
                    0
                )

                self.previous_gesture = gesture

            # FPS

            current_time = time.time()

            fps = 1 / (current_time - self.p_time)

            self.p_time = current_time

            self.fps_label.configure(
                text=f"FPS : {int(fps)}"
            )

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(rgb)

            img.thumbnail((1200, 850))

            imgtk = ImageTk.PhotoImage(img)

            self.camera_label.imgtk = imgtk

            self.camera_label.configure(
                image=imgtk
            )

        self.after(
            20,
            self.update_camera
        )

    def on_closing(self):

        self.cap.release()

        self.database.close()

        self.destroy()