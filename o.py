import sys
import random


class maze:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.grid = [[15 for _ in range(height)] for _ in range(width)]
        self.visited = [[False for _ in range(height)] for _ in range(width)]
        self.wall_color = "\033[34m"

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

    def get_neighbors(self, x, y) -> list:
        mylist = []
        if x - 1 >= 0:
            if not (self.visited[x - 1][y]):
                mylist += [(x - 1, y)]
        if y - 1 >= 0:
            if not self.visited[x][y - 1]:
                mylist += [(x, y - 1)]

        if y + 1 < self.height:
            if not self.visited[x][y + 1]:
                mylist += [(x, y + 1)]
        if x + 1 < self.width:
            if not self.visited[x + 1][y]:
                mylist += [(x + 1, y)]
        return mylist

    def dfs_generate(self, x, y):
        self.visited[x][y] = True

        neighbors = self.get_neighbors(x, y)
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if not self.visited[nx][ny]:
                self.remove_wall(x, y, nx, ny)
                self.dfs_generate(nx, ny)

    def get_direction(self, x, y):
        mylist = []
        if x - 1 >= 0 and (self.grid[x][y] & 8) == 0:
            mylist.append((x - 1, y, 'W'))
        if y - 1 >= 0 and (self.grid[x][y] & 1) == 0:
            mylist.append((x, y - 1, 'N'))
        if x + 1 < self.width and (self.grid[x][y] & 2) == 0:
            mylist.append((x + 1, y, 'S'))
        if y + 1 < self.height and (self.grid[x][y] & 4) == 0:
            mylist.append((x, y + 1, 'E'))
        return mylist

    def dfs_solver(self, x, y, exit_x, exit_y, path=None):
        if path is None:
            path = []
        self.visited[x][y] = True
        if (x, y) == (exit_x, exit_y):
            return True

        next = self.get_direction(x, y)
        if not next:
            return False

        for nx, ny, dir in next:
            if not self.visited[nx][ny]:
                path.append(dir)
                solution = self.dfs_solver(nx, ny, exit_x, exit_y, path)
                if solution:
                    return True
                path.pop()
        return False

    def display(self, entry=None, exit_node=None):
        print(self.wall_color + "+" + "---+" * self.width)
        for y in range(self.height):
            row = self.wall_color + "|"
            bottom = self.wall_color + "+"
            for x in range(self.width):
                cell = self.grid[x][y]
                content = "   "

                if (x, y) == entry:
                    content = "\033[41m S \033[0m"
                elif (x, y) == exit_node:
                    content = "\033[42m E \033[0m"

                row += content + (self.wall_color + "|" if cell & 4 else " ")
                bottom += (self.wall_color + "---+" if cell & 2 else "   +")

            print(row)
            print(bottom)


class MazeApp:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.maze = maze(int(self.config['WIDTH']), int(self.config['HEIGHT']))
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

        self.maze.dfs_generate(entry[0], entry[1])

        while True:
            self.maze.display(entry, exit_node)
            print("\nCommands: [R] Re-generate | [S] Solve | [Q] Quit")
            choice = input("Select an option: ").lower()

            if choice == 'r':
                self.maze = maze(self.maze.width, self.maze.height)
                self.maze.dfs_generate(entry[0], entry[1])
            elif choice == 's':
                print("Solving maze...")
                solution = []
                self.maze.dfs_solver(entry[0], entry[1], exit_node[0], exit_node[1], solution)
                # self.maze.save_to_file(entry, exit, solution)
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
