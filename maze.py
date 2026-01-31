import random
from collections import deque


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.wall_color = "\033[34m"

    def remove_wall(self, x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
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

    def print_42(self, x, y):
        matrix_42 = [
            [(0, 0), (0, 4), (0, 5), (0, 6)],
            [(1, 0), (1, 6)],
            [(2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6)],
            [(3, 2), (3, 4)],
            [(4, 2), (4, 4), (4, 5), (4, 6)]
        ]
        for i in matrix_42:
            for tup in i:
                self.visited[y + tup[0]][x + tup[1]] = True

    def get_nextors(self, x, y) -> list:
        mylist = []
        if x - 1 >= 0:
            if not (self.visited[y][x - 1]):
                mylist += [(y, x - 1)]
        if y - 1 >= 0:
            if not self.visited[y - 1][x]:
                mylist += [(y - 1, x)]

        if x + 1 < self.width:
            if not self.visited[y][x + 1]:
                mylist += [(y, x + 1)]
        if y + 1 < self.height:
            if not self.visited[y + 1][x]:
                mylist += [(y + 1, x)]
        return mylist

    def dfs_algo(self, x, y):
        self.visited[y][x] = True
        nextors = self.get_nextors(x, y)
        random.shuffle(nextors)
        for ny, nx in nextors:
            if not self.visited[ny][nx]:
                self.remove_wall(x, y, nx, ny)
                self.dfs_algo(nx, ny)

    def display(self, entry=None, exit_node=None, show_path=False, f="output_file.txt"):
        print(self.wall_color + "+" + "---+" * self.width)
        fi = open(f, "w")
        for y in range(self.height):
            row = self.wall_color + "|"
            bottom = self.wall_color + "+"
            for x in range(self.width):
                cell = self.grid[y][x]
                content = "   "
                if (x, y) == entry:
                    content = "\033[41m S \033[0m"
                elif (x, y) == exit_node:
                    content = "\033[42m E \033[0m"

                row += content + (self.wall_color + "|" if cell & 2 else " ")
                bottom += (self.wall_color + "---+" if cell & 4 else "   +")
                fi.write(hex(self.grid[y][x])[2:].upper())
            print(row)
            print(bottom)
            fi.write("\n")
        fi.write("\n")
        fi.write(f"{entry[0]},{entry[1]}\n")
        fi.write(f"{exit_node[0]},{exit_node[1]}\n")

    def solve(self, start_x, start_y, end_x, end_y):
        queue = deque([(start_x, start_y, [])])
        visited = set()
        visited.add((start_x, start_y))
        while queue:
            x, y, path = queue.popleft()
            if x == end_x and y == end_y:
                return path

            current_cell = self.grid[y][x]
            moves = [
                (0, -1, 'N', 1),
                (0, 1, 'S', 4),
                (1, 0, 'E', 2),
                (-1, 0, 'W', 8)
            ]
            for dx, dy, direction, wall_bits in moves:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (current_cell & wall_bits):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            new_path = path + [direction]
                            queue.append((nx, ny, new_path))
        return []


m = Maze(5, 5)
if m.height >= 12 and m.width >= 11:
    p_y = (m.height // 2) - (5 // 2)
    p_x = (m.width // 2) - (7 // 2)
    m.print_42(p_x, p_y)
m.dfs_algo(0, 0)
m.display((0, 0), (4, 4))
path = m.solve(0, 0, 4, 4)
print(path)
