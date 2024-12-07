import cv2
import pyautogui
import numpy as np
from PIL import ImageGrab
import time
import keyboard

FISH = (1116, 595, 1117, 721)
PLAYER = (1135, 595, 1139, 723)


def get_indicator(region):
    # Захват области экрана
    screen = np.array(ImageGrab.grab(bbox=region))
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # Перевод в градации серого
    return gray_screen


def save_debug_image(region, file_name):
    # Захват экрана
    screen = np.array(ImageGrab.grab(bbox=region))
    # Сохранение изображения
    cv2.imwrite(file_name, cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY))


def filter_color(image, lower_color, upper_color):
    # Преобразование в HSV (удобно для работы с цветами)
    # hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(image, lower_color, upper_color)  # Маска цвета
    return mask


def find_lowest_pixel(mask):
    coordinates = cv2.findNonZero(mask)  # Все пиксели, соответствующие маске
    if coordinates is not None:
        # Найти максимальную координату Y
        lowest_pixel = max(coordinates, key=lambda x: x[0][1])
        return lowest_pixel[0][1]  # Возврат координаты Y
    return None


def action(key_last='a', key_new='d'):
    pyautogui.keyUp(key_last)
    pyautogui.keyDown(key_new)


def fishing():
    pixel_height = None
    iteration = 0
    key_new = 'a'
    key_last = 'd'
    while True:
        image = get_indicator(FISH)
        max_y, max_intensity = find_brightest_pixel(image)
        print(pixel_height, max_y)
        if max_y is None:
            pyautogui.keyUp(key_last)
            break
        if pixel_height is None:
            pixel_height = max_y
            action()
        elif max_y - pixel_height <= 0:
            print('Изменение клавиши')
            action(key_last, key_new)
            key_last, key_new = key_new, key_last
            pixel_height = max_y
        else:
            print('Не изменилось')
            pixel_height = max_y
        time.sleep(0.2)
        iteration += 1
        print(f"Iteration: {iteration}, pixel_height: {pixel_height}")
        print()
        if iteration > 6:
            pyautogui.keyUp(key_last)
            time.sleep(0.4)
            pyautogui.keyDown(key_last)
            iteration = 0
        if keyboard.is_pressed('['):
            pyautogui.keyUp(key_last)
            break









def find_brightest_pixel(image):
    # Поиск яркости вдоль вертикальной линии
    max_intensity = np.max(image)  # Максимальная яркость
    max_y = np.argmax(image)  # Индекс максимальной яркости (строка)
    if max_intensity > 218:
        return max_y, max_intensity
    else:
        return None, None



if __name__ == '__main__':
    while True:
        if keyboard.is_pressed(']'):
            while True:
                fishing()
                print('Конец рыбалки')
                time.sleep(7)
                pyautogui.press('f')


                while True:
                    max_y, max_intensity = find_brightest_pixel(get_indicator(FISH))
                    print(max_y, max_intensity)
                    if max_y:
                        pyautogui.press('q')
                        break

