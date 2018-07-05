import pyperclip
import random
import pyautogui

# EN_TO_ES = {'-': '/', "'": '-', ':': 'º', }
EN_TO_ES = {}


def get_random_interval():
    """
    Disguise automation
    :return: interval between .05 and .15 second
    """
    # time for things to settle.
    base = .02
    return base + random.randint(0, 30)/1000


def translate_char(char):
    """Either there is no translation, and returns the same char or returns the value in the dictionary for the char"""
    return EN_TO_ES.get(char, char)


def translate(text):
    return ''.join([translate_char(c) for c in text])


def type(text: object, interval: object = get_random_interval()):
    text = translate(text)
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")


if __name__ == '__main__':
    # test it
    assert 'b' == translate('b')

    # type anything:
    print(translate('anything!'))

    # test typewritter
    type('avión con mucás tíldés')