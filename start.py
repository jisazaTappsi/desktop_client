import json
import requests
import pyautogui
import image_search
import spanish_typewritter


def request_messages():

    response = requests.get('https://peaku.co/dashboard/send_messages')

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

    search_bar_coordinates = image_search.find_search_bar()
    #search_bar_coordinates = (848, 99)

    contact_y_delta = 120

    erase_search_bar(search_bar_coordinates)

    for message in request_messages():

        user_name = message['fields']['contact_name']
        text = message['fields']['text']

        pyautogui.moveTo(*search_bar_coordinates)

        pyautogui.click()
        pyautogui.click()
        spanish_typewritter.type(user_name)

        contact_coordinates = search_bar_coordinates[0], search_bar_coordinates[1] + contact_y_delta
        pyautogui.moveTo(*contact_coordinates)
        pyautogui.click(interval=1)

        spanish_typewritter.type(text)
        pyautogui.press('enter')

        erase_search_bar(search_bar_coordinates)
