class Tail:
    def eval(self, args, pipeData):
        if (
            (len(args) != 1 and len(args) != 3 and not pipeData) or
            (pipeData and len(args) > 2)
        ):
            raise ValueError("wrong number of command line arguments")
        if len(args) == 1:
            num_lines = 10
            file = args[0]
        elif len(args) == 3:
            if args[0] != "-n":
                raise ValueError("wrong flags")
            else:
                num_lines = int(args[1])
                file = args[2]
        elif len(args) == 2 and pipeData:
            try:
                num_lines = int(args[1])
            except ValueError:
                raise ValueError("args[1] is not an integer")
        else:
            num_lines = 10
        result = ""
        if pipeData:
            lines = pipeData.split("\n")
            display_length = min(len(lines), num_lines)
            for i in range(0, display_length):
                result += lines[len(lines) - display_length + i] + "\n"
        else:
            try:
                with open(file) as f:
                    lines = f.readlines()
                    display_length = min(len(lines), num_lines)
                    for i in range(0, display_length):
                        result += lines[len(lines) - display_length + i]
            except FileNotFoundError as e:
                raise FileNotFoundError(f"File {file} not found: {e}")
        result = result.rstrip("\n")
        return result
