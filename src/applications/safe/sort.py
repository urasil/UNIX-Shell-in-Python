class Sort:
    def eval(self, args, pipeData):
        if (
            ((len(args) < 1 or len(args) > 2) and not pipeData) or
            (pipeData and len(args) > 1)
        ):
            raise ValueError("wrong number of command line arguments")
        reverseSorting = False
        if (len(args) == 2 and not pipeData) or (len(args) == 1 and pipeData):
            if '-' in args[0]:
                if args[0] == "-r":
                    reverseSorting = True
                    args.pop(0)
                else:
                    raise ValueError("Only the -r option is supported")
        lines = []
        result = ""

        if args:
            try:
                lines = open(args[0]).readlines()
            except FileNotFoundError:
                raise FileNotFoundError(f"File {args[0]} not found")
        else:
            lines = pipeData.split("\n")
            lines.pop()
        if not reverseSorting:
            lines.sort()
        else:
            lines.sort(reverse=True)
        for line in lines:
            line = line.rstrip("\n") + "\n"
            result += line
        # print("pipe:", pipeData)
        result = result.rstrip("\n")
        return result
