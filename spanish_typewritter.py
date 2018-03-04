import random
import pyautogui

EN_TO_ES = {'a': 'b'}


def get_random_interval():
    """
    Disguise automation
    :return: interval between .25 and .50 second
    """
    # time for things to settle.
    base = .25
    return base + random.randint(0, 20)/100


def translate_char(char):
    """Either there is no translation, and returns the same char or returns the value in the dictionary for the char"""
    return EN_TO_ES.get(char, char)


def translate(text):
    return ''.join([translate_char(c) for c in text])


def type(text):
    text = translate(text)
    pyautogui.typewrite(text, interval=get_random_interval())


if __name__ == '__main__':
    # test it
    assert 'b' == translate('b')

    # type anything:
    print(translate('anything!'))
