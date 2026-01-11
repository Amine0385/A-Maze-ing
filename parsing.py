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
                    if not line or '=' not in line:
                        continue

                    key, value = line.split('=')
                    self.params[key.strip()] = value.strip()

            self.width = int(self.params.get('WIDTH', 0))
            self.height = int(self.params.get('HEIGHT', 0))
            self.output_file = self.params.get('OUTPUT_FILE', 'output.txt')
            self.perfect = self.params.get('PERFECT', 'False') == 'True'

            entry_raw = self.params.get('ENTRY', '0,0').split(',')
            self.entry = (int(entry_raw[0]), int(entry_raw[1]))

            exit_raw = self.params.get('EXIT', '0,0').split(',')
            self.exit = (int(exit_raw[0]), int(exit_raw[1]))

        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error parsing config: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
    else:
        config = MazeConfig(sys.argv[1])
        print(f"Maze Size: {config.width}x{config.height}")