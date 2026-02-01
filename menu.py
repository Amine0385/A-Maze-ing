import sys
import random
from collections import deque
from parsing import Mazeconfig
from display import display


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: list[int] = [
            [15 for _ in range(width)]
            for _ in range(height)
        ]
        self.visited: list[bool] = [
            [False for _ in range(width)]
            for _ in range(height)
        ]
        self.wall_color: str = "\033[34m"

    def remove_wall(
            self, x1: int, y1: int, x2: int, y2: int
    ) -> None:
        dx: int = x2 - x1
        dy: int = y2 - y1
        if dx == 1:
            self.grid[y1][x1] &= ~2
            self.grid[y2][x2] &= ~8
        if dx == -1:
            self.grid[y1][x1] &= ~8
            self.grid[y2][x2] &= ~2
        if dy == 1:
            self.grid[y1][x1] &= ~4
            self.grid[y2][x2] &= ~1
        if dy == -1:
            self.grid[y1][x1] &= ~1
            self.grid[y2][x2] &= ~4


    def print_42(self):
        y = (self.height // 2) - (5 // 2)
        x = (self.width // 2) - (7 // 2)
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

    def get_nextors(self, x: int, y: int) -> list:
        mylist: list[tuple[int, int]] = []
        if x - 1 >= 0:
            if not self.visited[y][x - 1]:
                mylist.append((y, x - 1))
        if y - 1 >= 0:
            if not self.visited[y - 1][x]:
                mylist.append((y - 1, x))
        if x + 1 < self.width:
            if not self.visited[y][x + 1]:
                mylist.append((y, x + 1))
        if y + 1 < self.height:
            if not self.visited[y + 1][x]:
                mylist.append((y + 1, x))
        return mylist

    def dfs_algo(self, x: int, y: int) -> None:
        self.visited[y][x] = True
        nextors: list[tuple[int, int]] = self.get_nextors(x, y)
        random.shuffle(nextors)
        for ny, nx in nextors:
            if not self.visited[ny][nx]:
                self.remove_wall(x, y, nx, ny)
                self.dfs_algo(nx, ny)

    def solve(
        self, start_x: int, start_y: int, end_x: int, end_y: int
    ) -> list[str]:
        queue: list[tuple[int, int, list]] = deque([(start_x, start_y, [])])
        visited: set[int, int] = set()
        visited.add((start_x, start_y))
        while queue:
            x, y, path = queue.popleft()
            if x == end_x and y == end_y:
                return path
            current_cell = self.grid[y][x]
            move = [
                (0, -1, 'N', 1),
                (1, 0, 'E', 2),
                (0, 1, 'S', 4),
                (-1, 0, 'W', 8)
            ]
            for dx, dy, dir, wall_bit in move:
                nx: int = x + dx
                ny: int = y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (current_cell & wall_bit):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            new_path: list[str] = path + [dir]
                            queue.append((nx, ny, new_path))
        return []

    def main(self, param: dict, file_output: str, check: int):
        if check:
            random.seed(8)
        if not param["PERFECT"]:
            self.visited: list[bool] = [
                [False for _ in range(self.width)]
                for _ in range(self.height)
            ]
            if self.height >= 12 and self.width >= 11:
                self.print_42()
            self.dfs_algo(param["ENTRY"][0], param["ENTRY"][1])
        self.visited: list[bool] = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        if self.height >= 12 and self.width >= 11:
            self.print_42()
        self.dfs_algo(param["ENTRY"][0], param["ENTRY"][1])
        try:
            with open(file_output, "w") as fo:
                for i in range(self.height):
                    for j in range(self.width):
                        fo.write(str(hex(self.grid[i][j])[2:]).upper())
                    fo.write("\n")
                fo.write(f"\n{param['ENTRY'][0]},{param['ENTRY'][1]}\n")
                fo.write(f"{param['EXIT'][0]},{param['EXIT'][1]}\n")
                mylist = self.solve(
                    param['ENTRY'][0], param['ENTRY'][1],
                    param['EXIT'][0], param['EXIT'][1]
                )
                result = "".join(mylist)
                fo.write(f"{result}\n")
        except Exception:
            print("ERROR: cannot open the file")


def generate(check):

    ds = display()
    pars = Mazeconfig("config.txt")
    m = Maze(pars.param["WIDTH"], pars.param["HEIGHT"])
    param = pars.load_config("config.txt")
    m.main(param, pars.param["OUTPUT_FILE"], check)
    array = ds.display_bit(pars.param["OUTPUT_FILE"])
    if array:
        h = len(array)
        w = len(array[0])
        result = ds.draw_without_solve(array, w, h, pars.param["ENTRY"], pars.param["EXIT"])
        for row in result:
            print(row)


def solve_and_draw():
    ds = display()
    pars = Mazeconfig("config.txt")
    dir = ds.display_dir("maze.txt")
    cor = ds.create_solve_cor(pars.param["ENTRY"], dir)
    array = ds.display_bit("maze.txt")
    if array:
        h = len(array)
        w = len(array[0]) if h > 0 else 0
        result = ds.draw_with_solve(array, w, h, pars.param["ENTRY"], pars.param["EXIT"], cor)
        for row in result:
            print(row)


def menu():
    generate(1)
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. ")
        print("4. Quit")
        n = int(input())
        match n:
            case 1:
                generate(0)
            case 2:
                solve_and_draw()
            case 3:
                pass
            case 4:
                sys.exit()
            case _:
                pass


menu()
