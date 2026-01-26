import sys
import random


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

    def display(self, entry=None, exit_node=None, show_path=False):

        print(self.wall_color + "+" + "---+" * self.width)
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
            print(row)
            print(bottom)

    
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

        self.maze.generate(entry[0], entry[1])

        while True:
            self.maze.display(entry, exit_node)
            print("\nCommands: [R] Re-generate | [S] Solve | [Q] Quit")
            choice = input("Select an option: ").lower()

            if choice == 'r':
                self.maze = Maze(self.maze.width, self.maze.height)
                self.maze.generate(entry[0], entry[1])
            elif choice == 's':
                print("Solving maze...")
                solution = (
                    self.maze.solve
                    (entry[0], entry[1], exit_node[0], exit_node[1])
                )
                self.maze.save_to_file(entry, exit, solution)
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
