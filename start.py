import json
import time
import random
import requests
import pyautogui
import spanish_typewritter
import util
from cts import *

pyautogui.PAUSE = 1
CONTACT_DELTA_Y = 120


def get_random_interval():
    """
    Disguise automation
    :return: interval between .05 and .15 second
    """
    # time for things to settle.
    base = .02
    return base + random.randint(0, 30)/1000


def request_messages():

    response = requests.get('https://peaku.co/dashboard/send_messages')
    response.encoding = 'ISO-8859-1'

    data = json.loads(response.text)
    return json.loads(data)


def erase_search_bar(coordinates):

    pyautogui.moveTo(*coordinates)

    pyautogui.click(interval=0.1)
    pyautogui.click(interval=0.1)

    import platform

    if 'Darwin' in platform.platform():
        pyautogui.hotkey('command', 'a')
    else:
        pyautogui.hotkey('ctrl', 'a')

    pyautogui.press('backspace')


def send_message(message):
    # Removes any double spacing
    user_name = ' '.join(message['fields']['contact_name'].split())
    text = message['fields']['text']

    pyautogui.moveTo(*SEARCH_BAR_COORDINATES)

    pyautogui.click()
    pyautogui.click()
    pyautogui.typewrite(user_name, interval=get_random_interval())

    contact_coordinates = SEARCH_BAR_COORDINATES[0], SEARCH_BAR_COORDINATES[1] + CONTACT_DELTA_Y
    pyautogui.moveTo(*contact_coordinates)
    pyautogui.click(interval=1)

    spanish_typewritter.type(text)
    pyautogui.press('enter')

    erase_search_bar(SEARCH_BAR_COORDINATES)


def run():
    erase_search_bar(SEARCH_BAR_COORDINATES)
    message_queue = [m for m in request_messages()]

    while len(message_queue) > 0:

        # checks each second for a new message
        time.sleep(1)
        if util.messenger_running(SEARCH_BAR_COORDINATES):
            message = message_queue[0]
            message_queue = message_queue[1:]
            send_message(message)


if __name__ == '__main__':
    run()
