import numpy as np
from typing import List

class World:
    """
    Data structure for representing Game of Life worlds.
    """

    def __init__(self, width: int, height: int = -1):
        """
        Constructor of World datatype.

        :param width: integer representing the width of the world.
        :param height: (optional) integer representing the height of the world. If left implicit, the value of ``width`` is used to create a square-shaped world.
        """
        self.width = width
        if not height == -1:
            self.height = height
        else:
            self.height = width
        self.world = np.zeros((self.height, self.width), dtype=int)

    def get(self, x: int, y: int) -> int:
        """
        Returns the value on location ``(x, y)`` in the world.

        :param x: column-value of the location.
        :param y: row-value of the location.
        :return: value of location ``(x, y)`` in World.
        """
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return -1
        return self.world[y][x]

    def set(self, x: int, y: int, value:int = 1) -> None:
        """
        Sets the state of ``(x, y)`` to the given value.

        :param x: column-value of the location.
        :param y: row-value of the location.
        :param value: (optional) value to set location ``(x, y)``; uses ``1`` otherwise.
        """
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        self.world[y][x] = value

    def get_neighbours(self, x: int, y:int) -> List[int]:
        """
        Returns a list of values for the 8 neighbours of location ``(x, y)``.

        :param x: column-vale of the location.
        :param y: row-value of the location.
        :return: ``List`` of integers representing the values of the neighbours of ``(x, y)``.
        """
        neighbour_values = []
        for nx in range(x-1,x+2):
            for ny in range(y-1,y+2):
                if not (nx is x and ny is y):
                    neighbour_values.append(self.world[ny%self.height][nx%self.width])
        return neighbour_values

    def __str__(self):
        print('-'*self.width*4)
        for row in self.world:
            print('|', end=" ")
            for column in row:
                print(column, end=" | ")
            print()
            print('-'*self.width*4)
