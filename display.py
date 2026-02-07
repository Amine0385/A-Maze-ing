class display:
    def __init__(self, color_wall='\033[107m', forty2_color='\033[100m'):  # am
        self.START_COLOR = '\033[49m'
        self.FORTY2_COLOR = forty2_color
        self.WALL_COLOR = color_wall
        self.PATH_COLOR = '\033[49m'
        self.SOLVE_COLOR = '\033[48;5;94m'
        self.RESET = '\033[0m'

    def read_hex(self, filename):  # achraf
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

    def read_dir(self, filename):  # achraf
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

    def draw(self, array, width, height, entry, exit_node, solve=(), fla=1):
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
                if not (cell & 2):
                    matrix[cy][cx+1] = 0
                if not (cell & 4):
                    matrix[cy+1][cx] = 0
                if not (cell & 8):
                    matrix[cy][cx-1] = 0
                if (cell & 1) and (cell & 2) and (cell & 4) and (cell & 8):
                    matrix[cy][cx] = 2
        output = []
        solve_pixels = set()
        curr_x, curr_y = entry
        if fla % 2:
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
        for r in range(canvas_h):
            line = ""
            for c in range(canvas_w):
                is_wall = matrix[r][c] == 1
                is_42 = matrix[r][c] == 2
                is_entry = (r == entry[1] * 2 + 1 and c == entry[0] * 2 + 1)
                is_exit = (
                    r == exit_node[1] * 2 + 1 and c == exit_node[0] * 2 + 1)
                if fla % 2:
                    is_solve = (r, c) in solve_pixels
                if is_wall:
                    line += f"{self.WALL_COLOR}  {self.RESET}"
                elif is_entry:
                    line += f"{self.START_COLOR}🚕{self.RESET}"
                elif is_exit:
                    line += f"🏁{self.RESET}"
                elif is_42:
                    line += f"{self.FORTY2_COLOR}  {self.RESET}"
                elif fla % 2 and is_solve:
                    line += f"{self.SOLVE_COLOR}  {self.RESET}"
                else:
                    line += f"{self.PATH_COLOR}  {self.RESET}"
            output.append(line)
        return output

    def create_solve_cor(self, entry, str):  # amine
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
