import json
import random
import requests
import pyautogui
import image_search
import spanish_typewritter

pyautogui.PAUSE = 1


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


def erase_search_bar(search_bar_coordinates):

    pyautogui.moveTo(*search_bar_coordinates)

    pyautogui.click(interval=0.1)
    pyautogui.click(interval=0.1)

    import platform

    if 'Darwin' in platform.platform():
        pyautogui.hotkey('command', 'a')
    else:
        pyautogui.hotkey('ctrl', 'a')

    pyautogui.press('backspace')


if __name__ == '__main__':

    screenWidth, screenHeight = pyautogui.size()

    # search_bar_coordinates = image_search.find_search_bar()
    search_bar_coordinates = (848, 99)

    contact_y_delta = 120

    erase_search_bar(search_bar_coordinates)

    message_queue = [m for m in request_messages()]

    while len(message_queue) > 0:

        message = message_queue[0]
        message_queue = message_queue[1:]

        # Removes any double spacing
        user_name = ' '.join(message['fields']['contact_name'].split())
        text = message['fields']['text']

        pyautogui.moveTo(*search_bar_coordinates)

        pyautogui.click()
        pyautogui.click()
        pyautogui.typewrite(user_name, interval=get_random_interval())

        contact_coordinates = search_bar_coordinates[0], search_bar_coordinates[1] + contact_y_delta
        pyautogui.moveTo(*contact_coordinates)
        pyautogui.click(interval=1)

        spanish_typewritter.type(text)
        pyautogui.press('enter')

        erase_search_bar(search_bar_coordinates)
