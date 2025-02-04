from random import randint

import numpy as np
import pygame as pg


class Map:
    def __init__(self, min_peaks=6, max_peaks=12):
        self.height_map = self.__generate_height_map(min_peaks, max_peaks)

    def get_height_map(self):
        return self.height_map

    def __generate_height(self, height):
        if height <= 0:
            return np.int32(4095)

        return np.int32(int(hex(randint(height, height + 5))[2:] * 3, 16))

    def __generate_height_map(self, min_peaks, max_peaks):
        surface = pg.Surface((500, 500))
        surface.fill((0, 0, 0))

        height_map = pg.surfarray.array2d(surface)

        index_pairs = [(randint(0, 499), randint(0, 499)) for _ in range(randint(min_peaks, max_peaks))]
        big_pairs_count = len(index_pairs)
        index_pairs += [(randint(0, 499), randint(0, 499)) for _ in range(max_peaks)]

        for p in range(len(index_pairs)):
            height = randint(1, 255)

            min_x = index_pairs[p][0]
            max_x = index_pairs[p][0] + 1

            min_y = index_pairs[p][1]
            max_y = index_pairs[p][1] + 1

            if p != 0:
                if p < big_pairs_count:
                    peak_width = randint(75, 150)
                    
                else:
                    peak_width = randint(25, 60)

            while (min_x >= 0 or max_x < 501 or
                   min_y >= 0 or max_y < 501):

                for i in range(min_y, max_y):
                    if i < 0:
                        continue

                    elif i >= 500:
                        break

                    for j in range(min_x, max_x):
                        if (j < 0 or 
                            min_y < i < max_y - 1 and 
                            min_x < j < max_x - 1):
                            
                            continue

                        elif j >= 500:
                            break

                        height_map[j][i] = self.__generate_height(height)
            
                if height > 128:
                    height = randint(height - 10, height)

                else:
                    height = randint(height, height + 10)

                min_x = min_x - 1
                max_x = max_x + 1

                min_y = min_y - 1
                max_y = max_y + 1

                if p != 0 and (max_x - min_x + 1) // 2 > peak_width:
                    break

        return height_map
