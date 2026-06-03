import screen_brightness_control as sbc
import numpy as np


class BrightnessController:

    def __init__(self):
        pass

    def set_brightness_from_distance(
        self,
        distance,
        min_distance=30,
        max_distance=250
    ):

        brightness = np.interp(
            distance,
            [min_distance, max_distance],
            [0, 100]
        )

        brightness = int(brightness)

        try:
            sbc.set_brightness(brightness)
        except:
            pass

        return brightness

    def get_current_brightness(self):

        try:
            value = sbc.get_brightness()

            if isinstance(value, list):
                return value[0]

            return value

        except:
            return 0