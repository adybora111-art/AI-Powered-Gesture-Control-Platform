from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


class VolumeController:

    def __init__(self):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.volume = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

    def set_volume_from_distance(
        self,
        distance,
        min_distance=30,
        max_distance=250
    ):

        volume_percent = np.interp(
            distance,
            [min_distance, max_distance],
            [0, 100]
        )

        volume_percent = int(volume_percent)

        # Safety Limits
        if volume_percent < 0:
            volume_percent = 0

        if volume_percent > 100:
            volume_percent = 100

        # Windows Volume Control
        self.volume.SetMasterVolumeLevelScalar(
            volume_percent / 100,
            None
        )

        print(f"Volume: {volume_percent}%")

        return volume_percent

    def mute(self):

        self.volume.SetMute(
            1,
            None
        )

    def unmute(self):

        self.volume.SetMute(
            0,
            None
        )

    def get_current_volume(self):

        current = self.volume.GetMasterVolumeLevelScalar()

        return int(current * 100)