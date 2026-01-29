import sys
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


class MazeApp:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.maze = Maze(int(self.config['WIDTH']), int(self.config['HEIGHT']))
        self.run()

    def load_config(self, path):
        conf = {}
        with open(path, 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=')
                    conf[k.strip()] = v.strip()
        return conf

    def run(self):
        entry = tuple(map(int, self.config['ENTRY'].split(',')))
        exit_node = tuple(map(int, self.config['EXIT'].split(',')))
        output_file = open("output_file.txt", "a")
        self.maze.dfs_algo(entry[0], entry[1])

        while True:
            self.maze.display(entry, exit_node, "output_file.txt")
            print("\nCommands: [R] Re-generate | [S] Solve | [Q] Quit")
            choice = input("Select an option: ").lower()

            if choice == 'r':
                self.maze = Maze(self.maze.width, self.maze.height)
                self.maze.generate(entry[0], entry[1])
            elif choice == 's':
                print("Solving maze...")
                solution = self.maze.solve(entry[0], entry[1], exit_node[0], exit_node[1])

                with open("output_file.txt", "w") as f:
                    for row in self.maze.grid:
                        f.write("".join(f"{cell:X}" for cell in row) + "\n")

                    f.write("\n")
                    f.write(f"{entry[0]},{entry[1]}\n")
                    f.write(f"{exit_node[0]},{exit_node[1]}\n")

                    if solution:
                        f.write("".join(solution) + "\n")

                if solution:
                    print(f"Solution found! Steps: {len(solution)}")
                    print("Path: " + "".join(solution))
                else:
                    print("No solution found!")

                input("\nPress Enter to continue...")

            elif choice == 'q':
                break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        MazeApp(sys.argv[1])
    # m = Maze(6, 6)
    # m.dfs_generate(0, 0)
    # m.display((0, 0), (5, 5))
    # print(m.solve(0, 0, 5, 6))
