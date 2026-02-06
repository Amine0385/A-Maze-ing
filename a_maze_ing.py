import sys
from mazegen import Mazeconfig, MazeGenerator, display


def generate(ds, check, param):
    m = MazeGenerator(param["WIDTH"], param["HEIGHT"])
    m.main_generator(param, param["OUTPUT_FILE"], check)
    arr = ds.fprint_hex(param["OUTPUT_FILE"])
    if arr:
        h = len(arr)
        w = len(arr[0])
        result = ds.draw(
            arr, w, h, param["ENTRY"], param["EXIT"],)
        for row in result:
            print(row)


def solve_and_draw(ds, flag, param):
    dir = ds.display_dir(param["OUTPUT_FILE"])
    cor = ds.create_solve_cor(param["ENTRY"], dir)
    arr = ds.fprint_hex(param["OUTPUT_FILE"])
    if arr:
        h = len(arr)
        w = len(arr[0]) if h > 0 else 0
        result = ds.draw(
                arr, w, h, param["ENTRY"], param["EXIT"], cor, flag)
        for row in result:
            print(row)


def menu(param):
    ds = display()
    generate(ds, 1, param)
    flag = 1
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            n = int(input("choice? (1-4):> "))
            match n:
                case 1:
                    generate(ds, 0, param)
                    flag = 1
                case 2:
                    solve_and_draw(ds, flag, param)
                    flag += 1
                case 3:
                    print("choose your color for wall")
                    print("1. Purple")
                    print("2. green")
                    print("3. Blue")
                    print("4. back")
                    c = int(input("choice? (1-4):> "))
                    match c:
                        case 1:
                            ds.WALL_COLOR = '\033[105m'
                            ds.FORTY2_COLOR = '\033[107m'
                        case 2:
                            ds.WALL_COLOR = '\033[48;5;118m'
                            ds.FORTY2_COLOR = '\033[107m'
                        case 3:
                            ds.WALL_COLOR = '\033[48;5;117m'
                            ds.FORTY2_COLOR = '\033[105m'
                        case 4:
                            pass
                case 4:
                    sys.exit()
                case _:
                    print("Invalid option.")
        except ValueError:
            print("Please enter a number.")


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise Exception("You did not enter a file name")
        if sys.argv[1]:
            config = Mazeconfig(sys.argv[1])
            param = config.load_config(sys.argv[1])
            entry_x, entry_y = param["ENTRY"][0], param["ENTRY"][1]
            exit_x, exit_y = param["EXIT"][0], param["EXIT"][1]
            w, h = param["WIDTH"], param["HEIGHT"]
            if (entry_x < 0 or entry_y < 0) or (exit_x >= w or exit_y >= h):
                raise Exception("Entry or exit position is invalid ")
            menu(param)
    except Exception as e:
        print(e)
