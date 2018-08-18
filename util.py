from PIL import ImageGrab
from PIL import Image

from skimage.measure import compare_ssim as ssim
from skimage import img_as_float


def messenger_running(coordinates):

    screen = take_screen_shot()

    coordinate1 = coordinates[0] - 150, coordinates[1] - 20
    coordinate2 = coordinate1[0] + 299, coordinate1[1] + 39
    area = coordinate1 + coordinate2

    cropped_img = screen.crop(area)
    cropped_img.save('tmp2.png')
    cropped_img = img_as_float(cropped_img)

    search_bar = get_image('search_bar_es.png')
    similarity_active = ssim(img_as_float(search_bar), cropped_img, multichannel=True)

    connect_phone = get_image('deactive.png')
    similarity_inactive = ssim(img_as_float(connect_phone), cropped_img, multichannel=True)

    return similarity_active > similarity_inactive


def take_screen_shot():
    screen = ImageGrab.grab(bbox=None)
    screen.save('screen_shot.png')
    return screen #screen.convert("RGBA")


def get_image(path):
    return Image.open(path)
