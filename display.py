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

    def draw_with_solve(self, array, width, height, entry, exit_node, solve):
        START_COLOR = '\033[49m'
        WALL_COLOR = '\033[47m'
        PATH_COLOR = '\033[49m'
        SOLVE_COLOR = '\033[46m'
        RESET = '\033[0m'
        canvas_h = height * 2 + 1
        canvas_w = width * 2 + 1
        matrix = [[1 for _ in range(canvas_w)] for _ in range(canvas_h)]
        for y in range(height):
            for x in range(width):
                cell = array[y][x]
                cy = y * 2 + 1
                cx = x * 2 + 1
                matrix[cy][cx] = 0
                if not (cell & 1):
                    matrix[cy-1][cx] = 0
                if not (cell & 4):
                    matrix[cy+1][cx] = 0
                if not (cell & 8):
                    matrix[cy][cx-1] = 0
                if not (cell & 2):
                    matrix[cy][cx+1] = 0
        solve_pixels = set()
        curr_x, curr_y = entry

        for next_y, next_x in solve:
            p1_r = 2 * curr_y + 1
            p1_c = 2 * curr_x + 1
            p2_r = 2 * next_y + 1
            p2_c = 2 * next_x + 1

            solve_pixels.add((p2_r, p2_c))
            mid_r = (p1_r + p2_r) // 2
            mid_c = (p1_c + p2_c) // 2
            solve_pixels.add((mid_r, mid_c))
            curr_y, curr_x = next_y, next_x
        output = []
        for r in range(canvas_h):
            line = ""
            for c in range(canvas_w):
                is_wall = matrix[r][c] == 1
                is_entry = (r == entry[1] * 2 + 1 and c == entry[0] * 2 + 1)
                is_exit = (r == exit_node[1] * 2 + 1 and c == exit_node[0] * 2 + 1)
                is_solve = (r, c) in solve_pixels
                if is_wall:
                    line += f"{WALL_COLOR}  {RESET}"
                elif is_entry:
                    line += f"{START_COLOR}🚕{RESET}"
                elif is_exit:
                    line += f"🏁{RESET}"
                elif is_solve:
                    line += f"{SOLVE_COLOR}  {RESET}"
                else:
                    line += f"{PATH_COLOR}  {RESET}"
            output.append(line)
        return output

    def draw_without_solve(self, array, width, height, entry, exit_node):
        START_COLOR = '\033[49m'
        WALL_COLOR = '\033[47m'
        PATH_COLOR = '\033[49m'
        RESET = '\033[0m'
        canvas_h = height * 2 + 1
        canvas_w = width * 2 + 1
        matrix = [[1 for _ in range(canvas_w)] for _ in range(canvas_h)]
        for y in range(height):
            for x in range(width):
                cell = array[y][x]
                cy = y * 2 + 1
                cx = x * 2 + 1
                matrix[cy][cx] = 0
                if not (cell & 1):
                    matrix[cy-1][cx] = 0
                if not (cell & 4):
                    matrix[cy+1][cx] = 0
                if not (cell & 8):
                    matrix[cy][cx-1] = 0
                if not (cell & 2):
                    matrix[cy][cx+1] = 0
        output = []
        for r in range(canvas_h):
            line = ""
            for c in range(canvas_w):
                is_wall = matrix[r][c] == 1
                is_entry = (r == entry[1] * 2 + 1 and c == entry[0] * 2 + 1)
                is_exit = (r == exit_node[1] * 2 + 1 and c == exit_node[0] * 2 + 1)
                if is_wall:
                    line += f"{WALL_COLOR}  {RESET}"
                elif is_entry:
                    line += f"{START_COLOR}🚕{RESET}"
                elif is_exit:
                    line += f"🏁{RESET}"
                else:
                    line += f"{PATH_COLOR}  {RESET}"
            output.append(line)
        return output

    def create_solve_cor(self, entry, str):
        x, y = entry
        mylist = []
        for i in str:
            if i == 'S':
                y += 1
                mylist.append((y, x))
            if i == 'N':
                y -= 1
                mylist.append((y, x))
            if i == 'W':
                x -= 1
                mylist.append((y, x))
            if i == 'E':
                x += 1
                mylist.append((y, x))
        return mylist


# if __name__ == "__main__":
#     from parsing import Mazeconfig
#     pars = Mazeconfig("config.txt")
#     entry = pars.param.get("ENTRY", [0, 1])
#     exit_node = pars.param.get("EXIT", [12, 12])
#     m = display()
#     str = m.display_dir("maze.txt")
#     cor = m.create_solve_cor(entry, str)
#     array = m.display_bit("maze.txt")
#     if array:
#         h = len(array)
#         w = len(array[0]) if h > 0 else 0
#         result = m.draw_without_solve(array, w, h, entry, exit_node)
#         for row in result:
#             print(row)