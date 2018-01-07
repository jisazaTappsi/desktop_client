import json
import random
import requests
import pyautogui
import image_search


def request_messages():

    response = requests.get('https://peaku.co/dashboard/send_messages')

    data = json.loads(response.text)
    data = json.loads(data)
    print(data)

    return data['message'], data['users']


def get_random_interval():
    """
    Diguise automation
    :return: interval between .25 and 1.25 second
    """
    # time for things to settle.
    base = .25
    return base + random.randint(0, 1000)/1000


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

    message, users = request_messages()

    screenWidth, screenHeight = pyautogui.size()

    search_bar_coordinates = image_search.find_search_bar()
    #search_bar_coordinates = (848, 99)

    contact_y_delta = 120

    erase_search_bar(search_bar_coordinates)

    for u in users:

        user_name = u['fields']['name'] + ' ' + str(u['pk'])

        pyautogui.moveTo(*search_bar_coordinates)

        pyautogui.click()
        pyautogui.click()
        pyautogui.typewrite(user_name, interval=0.1)

        contact_coordinates = search_bar_coordinates[0], search_bar_coordinates[1] + contact_y_delta
        pyautogui.moveTo(*contact_coordinates)
        pyautogui.click(interval=1)

        pyautogui.typewrite(message, interval=get_random_interval())
        pyautogui.press('enter')

        erase_search_bar(search_bar_coordinates)