import sys


class MazeConfig:
    def __init__(self, filepath):
        self.params = {}
        self.load_config(filepath)

    def load_config(self, filepath):
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue

                    key, value = line.split('=', 1)
                    self.params[key.strip()] = value.strip()

            mandatory = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE']
            for key in mandatory:
                if key not in self.params:
                    print(f"Error: {key} is missing from config.")
                    sys.exit(1)

            try:
                self.width = int(self.params['WIDTH'])
                self.height = int(self.params['HEIGHT'])
                self.output_file = self.params['OUTPUT_FILE']
                self.perfect = self.params.get('PERFECT', 'False') == 'True'

                e_x, e_y = self.params['ENTRY'].split(',')
                self.entry = (int(e_x), int(e_y))

                ex_x, ex_y = self.params['EXIT'].split(',')
                self.exit = (int(ex_x), int(ex_y))
            except ValueError:
                print(
                    "Error: WIDTH, HEIGHT, and Coordinates must be integers.")
                sys.exit(1)

        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            sys.exit(1)
