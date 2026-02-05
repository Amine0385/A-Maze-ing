import sys
from mazegen import Mazeconfig, MazeGenerator, display


def generate(ds, check, file_input, pars):
    m = MazeGenerator(pars.param["WIDTH"], pars.param["HEIGHT"])
    param = pars.load_config(file_input)
    m.main_generator(param, pars.param["OUTPUT_FILE"], check)
    array = ds.display_bit(pars.param["OUTPUT_FILE"])
    if array:
        h = len(array)
        w = len(array[0])
        result = ds.draw_without_solve(
            array, w, h, pars.param["ENTRY"], pars.param["EXIT"])
        for row in result:
            print(row)


def solve_and_draw(ds, flag, pars):
    dir = ds.display_dir(pars.param["OUTPUT_FILE"])
    cor = ds.create_solve_cor(pars.param["ENTRY"], dir)
    array = ds.display_bit(pars.param["OUTPUT_FILE"])
    if array:
        h = len(array)
        w = len(array[0]) if h > 0 else 0
        if flag % 2:
            result = ds.draw_with_solve(
                array, w, h, pars.param["ENTRY"], pars.param["EXIT"], cor)
        else:
            result = ds.draw_without_solve(
                array, w, h, pars.param["ENTRY"], pars.param["EXIT"])
        for row in result:
            print(row)


def menu(file_input, pars):
    ds = display()
    generate(ds, 1, file_input, pars)
    flag = 1
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. [Reserved]")
        print("4. Quit")

        try:
            n = int(input("> "))
            match n:
                case 1:
                    generate(ds, 0, file_input, pars)
                    flag = 1
                case 2:
                    solve_and_draw(ds, flag, pars)
                    flag += 1
                case 3:
                    print("Option 3 is not implemented yet.")
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
            pars = Mazeconfig(sys.argv[1])
            menu(sys.argv[1], pars)

    except Exception as e:
        print(e)
