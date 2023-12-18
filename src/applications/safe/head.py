class Head:
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
                try:
                    num_lines = int(args[1])
                    file = args[2]
                except ValueError:
                    raise ValueError("args[1] is not an integer")
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
            for i in range(0, min(len(lines), num_lines)):
                result += lines[i] + "\n"
        else:
            try:
                with open(file) as f:
                    lines = f.readlines()
                    for i in range(0, min(len(lines), num_lines)):
                        result += lines[i]
            except FileNotFoundError as e:
                raise FileNotFoundError(f"File {file} not found: {e}")
        return result
