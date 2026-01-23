import random


def generate(self, x, y):
    self.visited[y][x] = True
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
            if not self.visited[ny][nx]:
                self.remove_wall(x, y, nx, ny)
                self.generate(nx, ny)
