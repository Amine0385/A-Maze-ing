import random


class Maze:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.grid = [[15 for _ in range(height)] for _ in range(width)]
        self.visited = [[False for _ in range(height)] for _ in range(width)]

    def remove_wall(self, x1, y1, x2, y2) -> None:
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1:
            self.grid[x1][y1] &= ~4
            self.grid[x2][y2] &= ~1
        elif dx == -1:
            self.grid[x1][y1] &= ~1
            self.grid[x2][y2] &= ~4
        elif dy == 1:
            self.grid[x1][y1] &= ~2
            self.grid[x2][y2] &= ~8
        elif dy == -1:
            self.grid[x1][y1] &= ~8
            self.grid[x2][y2] &= ~2


def get_neighbors(width, height, x, y, visited) -> list:
    mylist = []
    if x - 1 >= 0:
        if not visited[x - 1][y]:
            mylist += [(x - 1, y)]
    if y - 1 >= 0:
        if not visited[x][y - 1]:
            mylist += [(x, y - 1)]

    if x + 1 < width:
        if not visited[x + 1][y]:
            mylist += [(x + 1, y)]
    if y + 1 < height:
        if not visited[x][y + 1]:
            mylist += [(x, y + 1)]
    return mylist


m = Maze(6, 7)

m.remove_wall(0, 0, 1, 0)
m.remove_wall(5, 6, 5, 5)
for i in m.grid:
    print(i)