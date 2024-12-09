import time

import cv2
import keyboard
import numpy as np
import pyautogui
from PIL import ImageGrab

FISH = (1116, 595, 1117, 721)


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


def main():
    while True:
        if keyboard.is_pressed(']'):
            while True:
                pyautogui.press('f')
                while True:
                    max_y, max_intensity = find_brightest_pixel(get_indicator(FISH))
                    print(max_y, max_intensity)
                    if max_y:
                        if 0 < max_y < 5:
                            pyautogui.press('q')
                            fishing()
                            print('Конец рыбалки')
                            time.sleep(5)
                            break



if __name__ == '__main__':
    main()
