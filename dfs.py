import random


def generate(self, x=0, y=0):
    self.visited[y][x] = True

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
            if not self.visited[ny][nx]:
                self.remove_wall(x, y, nx, ny)
                self.generate(nx, ny)


def display(self):
    print("+" + "---+" * self.width)
    for y in range(self.height):
        row = "|"
        bottom = "+"
        for x in range(self.width):
            cell = self.grid[y][x]
            row += "   " + ("|" if cell & 2 else " ")
            bottom += ("---+" if cell & 4 else "   +")
        print(row)
        print(bottom)
