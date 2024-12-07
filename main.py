from processing import *
import time

while True:
    max_p, intensive = find_brightest_pixel(get_indicator(FISH))
    print(max_p, intensive)
    time.sleep(1)


