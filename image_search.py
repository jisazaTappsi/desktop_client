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
TOPS = 5


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
    return screen.convert("RGBA")


def get_image(path):
    return Image.open(path)


def get_matrix(all_similarities, number_columns):
    a = np.array(all_similarities)
    a.shape = a.shape = (a.size // number_columns, number_columns)
    return a


def do_image_analysis(coordinate_x, coordinate_y, result):

    coordinate1 = coordinate_x, coordinate_y
    coordinate2 = coordinate1[0] + result.image_width, coordinate1[1] + result.image_height
    area = coordinate1 + coordinate2

    cropped_img = result.screen.crop(area)
    #cropped_img.save('tmp.png')

    similarity = ssim(img_as_float(result.image_to_match), img_as_float(cropped_img), multichannel=True)

    binarized_img = binarize_image(cropped_img, THRESHOLD)
    text = pytesseract.image_to_string(binarized_img)
    print('image analysis done, reads: ' + text)

    text_similarities = []
    for possible_text in SEARCH_TEXTS:
        text_similarities.append(get_text_similarity(text, possible_text))
    similarity += max(text_similarities)

    similarity = int(similarity * 1000)
    result.all_similarities.append(similarity)

    if result.max_similarity < similarity:
        result.max_similarity = similarity
        result.best_img = cropped_img
        result.best_area = area

    return result


def show_results(result):

    result.best_img.save('best_img_{area}_{sim}.png'.format(area=result.best_area, sim=result.max_similarity))

    print('num cols: ' + str(result.get_num_columns()))
    print('num rows: ' + str(result.get_num_rows()))


def get_top_coordinates(result):

    m = get_matrix(result.all_similarities, number_columns=result.get_num_columns())
    max_y, max_x = m.shape
    print(m)

    tops = sorted(result.all_similarities)[-TOPS:]

    for t in tops:
        y_array, x_array = np.where(m == t)
        x = x_array[0]
        y = y_array[0]

        # Search Neighbors.
        from_x, from_y = result.get_pixels_for_coordinate(x-1, y-1, max_x, max_y)
        to_x, to_y = result.get_pixels_for_coordinate(x+1, y+1, max_x, max_y)

        result.increase_x = result.image_width/5
        result.increase_y = result.image_height/5

        result = scan_image_area(result, to_x=to_x, to_y=to_y, from_x=from_x, from_y=from_y)

    return result


class Result:

    def __init__(self, increase_x, increase_y, image_to_match, screen):
        self.increase_x = increase_x
        self.increase_y = increase_y

        self.image_to_match = image_to_match
        self.image_width, self.image_height = image_to_match.size

        self.screen = screen
        self.screen_width, self.screen_height = screen.size

        self.best_img = None
        self.best_area = None
        self.max_similarity = 0
        self.all_similarities = []

    def get_num_columns(self):
        return self.screen_width//self.increase_x

    def get_num_rows(self):
        return self.screen_height//self.increase_y

    def get_pixels_for_coordinate(self, column, row, total_columns, total_rows):
        """Goes from matrix (column, row) to pixels."""
        return int(column/total_columns*self.screen_width), int(row/total_rows*self.screen_height)


def scan_image_area(result, to_x, to_y, from_x=0, from_y=0):

    coordinate_y = from_y
    while coordinate_y + result.image_height < to_y:

        coordinate_x = from_x
        while coordinate_x + result.image_width < to_x:
            result = do_image_analysis(coordinate_x, coordinate_y, result)

            coordinate_x += result.increase_x

        coordinate_y += result.increase_y

    return result


def get_coordinates(image_to_match):

    screen = take_screen_shot()
    image_width, image_height = image_to_match.size

    increase_y = int(image_height / 2)
    increase_x = int(image_width / 1)

    result = Result(increase_x, increase_y, image_to_match, screen)

    result = scan_image_area(result, to_x=result.screen_width, to_y=result.screen_height)

    show_results(result)

    result = get_top_coordinates(result)

    show_results(result)

    return (int(result.best_area[0] + result.best_area[2])/2), int((result.best_area[1] + result.best_area[3])/2)


def find_search_bar():
    """
    :return: pair of coordinates to click on search bar.
    """

    # set threshold
    #binarized_img = binarize_image(search_bar, THRESHOLD)
    #sample_text = pytesseract.image_to_string(binarized_img)
    #print('sample text: ' + sample_text)
    #print('sample text similarity: ' + str(get_text_similarity(sample_text)))

    return get_coordinates(get_image('search_bar_es.png'))
