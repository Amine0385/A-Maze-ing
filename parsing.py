class Mazeconfig:  # achraf
    def __init__(self) -> None:
        self.param: dict = {}
        # self.load_config(filename)

    def load_config(self, filename: str) -> dict:
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        try:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()

                            if key.upper() in ("WIDTH", "HEIGHT"):
                                self.param[key] = int(value)
                            elif key.upper() in ("ENTRY", "EXIT"):
                                self.param[key] = [
                                    int(x.strip()) for x in value.split(",")]
                            elif key.upper() == "OUTPUT_FILE":
                                self.param[key] = value
                            elif key.upper() == "PERFECT":
                                self.param[key] = value.upper() == "TRUE"
                        except Exception as e:
                            print(f"Error parsing line '{line}': {e}")
                            return None
            return self.param
        except Exception:
            print("ERROR: cannot open the file")
        print(self.param)
