class display():
    def __init__(self):
        pass

    def display_bit(self, filename):
        try:
            mylist = []
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or "," in line:
                        break
                    new_line = []
                    for c in line:
                        try:
                            new_line.append(int(c, 16))
                        except ValueError:
                            continue
                    if new_line:
                        mylist.append(new_line)
                return mylist
        except Exception as e:
            print(f"Error reading bit map: {e}")
            return []

    def display_dir(self, filename):
        try:
            flag = 0
            with open(filename, "r") as f:
                for line in f:
                    if "," in line:
                        flag = 1
                    if flag == 1:
                        if "," not in line:
                            return line.strip()
        except Exception as e:
            print(e)
            return []

    def draw(self, array, width, height, entry, exit_node, solve):
        START_COLOR = '\033[41m'
        WALL_COLOR = '\033[47m'
        PATH_COLOR = '\033[49m'
        SOLVE_COLOR = '\033[46m'
        RESET = '\033[0m'
        canvas_h = height * 2 + 1
        canvas_w = width * 2 + 1
        canvas = [[1 for _ in range(canvas_w)] for _ in range(canvas_h)]
        for y in range(height):
            for x in range(width):
                cell = array[y][x]
                cy = y * 2 + 1
                cx = x * 2 + 1
                canvas[cy][cx] = 0
                if not (cell & 1):
                    canvas[cy-1][cx] = 0
                if not (cell & 4):
                    canvas[cy+1][cx] = 0
                if not (cell & 8):
                    canvas[cy][cx-1] = 0
                if not (cell & 2):
                    canvas[cy][cx+1] = 0
        output = []
        for r in range(canvas_h):
            line = ""
            for c in range(canvas_w):
                is_wall = canvas[r][c] == 1
                is_entry = False
                is_exit = False
                is_solve = False
                cell_y = (r - 1) // 2
                cell_x = (c - 1) // 2
                if not is_wall and 0 <= cell_y < height:
                    if 0 <= cell_x < width:
                        if (cell_x, cell_y) == tuple(entry):
                            is_entry = True
                        elif (cell_x, cell_y) == tuple(exit_node):
                            is_exit = True
                        for tup in solve:
                            if (cell_y, cell_x) == tuple(tup):
                                is_solve = True
                                break
                if is_wall:
                    line += f"{WALL_COLOR}  {RESET}"
                elif is_entry:
                    line += f"{START_COLOR}  {RESET}"
                elif is_exit:
                    line += f"{START_COLOR}  {RESET}"
                elif is_solve:
                    line += f"{SOLVE_COLOR}  {RESET}"
                else:
                    line += f"{PATH_COLOR}  {RESET}"
            output.append(line)

        return output

    def create_solve_cor(self, entry, str):
        y, x = entry
        mylist = []
        for i in str:
            if i == 'S':
                tup1 = (y + 1, x)
                mylist.append(tup1)
                y = y + 1
            if i == 'N':
                tup1 = (y - 1, x)
                mylist.append(tup1)
                y = y - 1
            if i == 'W':
                tup1 = (y, x - 1)
                mylist.append(tup1)
                x = x - 1
            if i == 'E':
                tup2 = (y, x + 1)
                mylist.append(tup2)
                x = x + 1
        return mylist


if __name__ == "__main__":
    from parsing import Mazeconfig
    pars = Mazeconfig("config.txt")
    entry = pars.param.get("ENTRY", [0, 1])
    exit_node = pars.param.get("EXIT", [12, 12])
    m = display()
    str = m.display_dir("maze.txt")
    cor = m.create_solve_cor(entry, str)
    array = m.display_bit("maze.txt")
    if array:
        h = len(array)
        w = len(array[0]) if h > 0 else 0
        result = m.draw(array, w, h, entry, exit_node, cor)
        for row in result:
            print(row)

