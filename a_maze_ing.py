class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def remove_wall(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1:
            self.grid[y1][x1] &= ~2
            self.grid[y2][x2] &= ~8
        elif dx == -1:
            self.grid[y1][x1] &= ~8
            self.grid[y2][x2] &= ~2
        elif dy == 1:
            self.grid[y1][x1] &= ~4
            self.grid[y2][x2] &= ~1
        elif dy == -1:
            self.grid[y1][x1] &= ~1
            self.grid[y2][x2] &= ~4

    def display(self):
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row_str = "|"
            bottom_str = "+"
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell & 2:
                    row_str += "   |"
                else:
                    row_str += "    "
                if cell & 4:
                    bottom_str += "---+"
                else:
                    bottom_str += "   +"
            print(row_str)
            print(bottom_str)


m = Maze(5, 5)
m.remove_wall(0, 0, 0, 1)
m.display()
