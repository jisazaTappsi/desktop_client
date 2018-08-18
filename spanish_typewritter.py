import pyperclip
import random
import pyautogui
import platform


def get_random_interval():
    """
    Disguise automation
    :return: interval between .05 and .15 second
    """
    # time for things to settle.
    base = .02
    return base + random.randint(0, 30)/1000


def type(text):
    pyperclip.copy(text)
    if platform.system() == 'Darwin':
        pyautogui.hotkey("command", "v")
    else:
        pyautogui.hotkey("ctrl", "v")


if __name__ == '__main__':

    # test typewritter
    type('avión con mucás tíldés')
