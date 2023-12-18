class Uniq:
    def eval(self, args, pipeData):
        if (
            ((len(args) < 1 or len(args) > 2) and not pipeData) or
            (pipeData and len(args) > 1)
        ):
            raise ValueError("wrong number of command line arguments")
        ignoreCase = False
        lines = []
        if (len(args) == 2 and not pipeData) or (len(args) == 1 and pipeData):
            if args[0] == "-i":
                ignoreCase = True
                args.pop(0)
        lines = []

        if args:
            try:
                lines = open(args[0]).readlines()
            except FileNotFoundError:
                raise FileNotFoundError(f"File {args[0]} not found")
        else:
            lines = pipeData.split("\n")

        uniqueLines = []
        for line in lines:
            line = line.rstrip("\n") + "\n"
            comparisonLine = line.lower() if ignoreCase else line

            if len(uniqueLines) > 0:
                if not ignoreCase and comparisonLine != uniqueLines[-1]:
                    uniqueLines.append(line.rstrip("\n") + "\n")
                else:
                    if (
                        ignoreCase and
                        comparisonLine != uniqueLines[-1].lower()
                    ):
                        uniqueLines.append(line.rstrip("\n") + "\n")
            else:
                uniqueLines.append(line.rstrip("\n") + "\n")
        result = "".join(uniqueLines)
        result = result.rstrip("\n")
        return result
