import pyautogui
from skimage.measure import compare_ssim as ssim
from skimage import img_as_float
import time

import spanish_typewritter
import start
import util
from cts import *


if __name__ == '__main__':

    contact_y_delta = 120
    start.erase_search_bar(SEARCH_BAR_COORDINATES)

    message_queue = ['prúébá ññññ del robot (que pena molestarlo, jajajaj)1',
                     'prúébá ññññ del robot (que pena molestarlo, jajajaj)2',
                     'prúébá ññññ del robot (que pena molestarlo, jajajaj)3',
                     'prúébá ññññ del robot (que pena molestarlo, jajajaj)4',
                     'prúébá ññññ del robot (que pena molestarlo, jajajaj)5',
                     'prúébá ññññ del robot (que pena molestarlo, jajajaj)6',
                     'prúébá ññññ del robot (que pena molestarlo, jajajaj)7 TERMINO',
                     ]

    while len(message_queue) > 0:
        if util.messenger_running(SEARCH_BAR_COORDINATES):

            # Removes any double spacing
            user_name = 'Santiago Paisa Nuevo Gonzales'

            text = message_queue[0]
            message_queue = message_queue[1:]

            pyautogui.moveTo(*SEARCH_BAR_COORDINATES)

            pyautogui.click()
            pyautogui.click()
            pyautogui.typewrite(user_name, interval=start.get_random_interval())

            contact_coordinates = SEARCH_BAR_COORDINATES[0], SEARCH_BAR_COORDINATES[1] + contact_y_delta
            pyautogui.moveTo(*contact_coordinates)
            pyautogui.click(interval=1)

            spanish_typewritter.type(text)
            pyautogui.press('enter')

            start.erase_search_bar(SEARCH_BAR_COORDINATES)
        time.sleep(1)
