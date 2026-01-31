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

    def draw(self, array, width, height, entry, exit):
        WALL_COLOR = '\033[47m'
        PATH_COLOR = '\033[40m'
        START_COLOR = '\033[45m'
        EXIT_COLOR = '\033[41m'
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
        flag1 = 0
        flag2 = 0
        for r in range(canvas_h):
            line = ""
            for c in range(canvas_w):
                is_wall = canvas[r][c] == 1
                is_entry = False
                is_exit = False
                cell_y = (r - 1) // 2
                cell_x = (c - 1) // 2
                
                if not is_wall and 0 <= cell_y < height and 0 <= cell_x < width:
                    if (cell_x, cell_y) == tuple(entry):
                        is_entry = True
                    elif (cell_x, cell_y) == tuple(exit):
                        is_exit = True
                if is_wall:
                    line += f"{WALL_COLOR}  {RESET}"
                elif is_entry and flag1 == 0:
                    flag1 = 1
                    line += f"{START_COLOR}  {RESET}"
                elif is_exit and flag2 == 0:
                    flag2 = 1
                    line += f"{EXIT_COLOR}  {RESET}"
                else:
                    line += f"{PATH_COLOR}  {RESET}"
            output.append(line)

        return output

if __name__ == "__main__":
    from parsing import Mazeconfig
    
    # Load config to get Start/Exit
    pars = Mazeconfig("config.txt")
    entry = pars.param.get("ENTRY", [0, 0])
    exit = pars.param.get("EXIT", [11, 11])

    m = display()
    array = m.display_bit("maze.txt")
    
    if array:
        h = len(array)
        w = len(array[0]) if h > 0 else 0
        result = m.draw(array, w, h, entry, exit)

        for row in result:
            print(row)
        print(m.display_dir("maze.txt"))