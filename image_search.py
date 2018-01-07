import distance
import pytesseract
import numpy as np
from PIL import Image
from PIL import ImageGrab
from skimage.measure import compare_ssim as ssim
from skimage import img_as_float
from scipy.misc import imsave

SEARCH_TEXTS = {'search or start new chat', 'Buscar o empezar un chat nuevo'}
CHAT_BAR_TEXT = 'Type a message'
THRESHOLD = 220


def binarize_array(numpy_array, threshold=100):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array


def binarize_image(image, threshold):
    """Binarize an image."""
    image = image.convert('L')  # convert image to monochrome
    image = np.array(image)
    arrays = binarize_array(image, threshold)
    #min_value = min([min(a) for a in arrays])
    #max_value = max([max(a) for a in arrays])
    imsave('binarized_image.jpg', arrays)
    return Image.open('binarized_image.jpg')#, min_value, max_value


def get_text_similarity(text, text_to_match):
    #return distance.levenshtein(text1, text2)
    return 1 - distance.levenshtein(text, text_to_match) / len(text_to_match)

    #distance.hamming("hamming", "hamning")
    #distance.nlevenshtein("abc", "acd", method=1)  # shortest alignment
    #distance.nlevenshtein("abc", "acd", method=2)  # longest alignment
    #distance.sorensen("decide", "resize")
    #distance.jaccard("decide", "resize")


def take_screen_shot():
    screen = ImageGrab.grab(bbox=None)
    screen.save('screen_shot.png')
    screen.convert("RGBA")
    return screen


def get_image(path):
    return Image.open(path)


def get_coordinates(texts_to_match, image_to_match):

    screen = take_screen_shot()
    screen_width, screen_height = screen.size

    image_width, image_height = image_to_match.size

    best_img = None
    best_area = None
    max_similarity = 0

    coordinate_x = 0
    while coordinate_x + image_width < screen_width:

        coordinate_y = 0
        while coordinate_y + image_height < screen_height:

            coordinate1 = coordinate_x, coordinate_y
            coordinate2 = coordinate1[0] + image_width, coordinate1[1] + image_height
            area = coordinate1 + coordinate2

            cropped_img = screen.crop(area)
            #cropped_img.save('auto_messenger/tmp.png')

            similarity = ssim(img_as_float(image_to_match), img_as_float(cropped_img), multichannel=True)

            binarized_img = binarize_image(cropped_img, THRESHOLD)
            text = pytesseract.image_to_string(binarized_img)

            for possible_text in texts_to_match:
                similarity += get_text_similarity(text, possible_text)

            similarity = int(similarity*1000)

            #print(similarity)

            #if cropped_img:
            #    cropped_img.save('tmp_best_img_{area}_{sim}.png'.format(area=area, sim=similarity))

            if max_similarity < similarity:
                max_similarity = similarity
                best_img = cropped_img
                best_area = area

            coordinate_y += int(image_height/2)

        coordinate_x += int(image_width / 2)

    best_img.save('best_img_{area}_{sim}.png'.format(area=best_area, sim=max_similarity))

    return (int(best_area[0] + best_area[2])/2), int((best_area[1] + best_area[3])/2)


def find_search_bar():
    """
    :return: pair of coordinates to click on search bar.
    """

    # set threshold
    #binarized_img = binarize_image(search_bar, THRESHOLD)
    #sample_text = pytesseract.image_to_string(binarized_img)
    #print('sample text: ' + sample_text)
    #print('sample text similarity: ' + str(get_text_similarity(sample_text)))

    return get_coordinates(SEARCH_TEXTS, get_image('search_bar.png'))


def find_contact(contact_name, search_area):
    """
    :param contact_name:
    :param search_area:
    :return:
    """
    screen = take_screen_shot()
    contact_height = 100

    coor_y = search_area[1]
    while coor_y + contact_height < screen.height:
        pass
