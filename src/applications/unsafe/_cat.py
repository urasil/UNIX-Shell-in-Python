class _Cat:
    def eval(self, args, pipeData):
        # print("cat eval")
        lines = []
        result = ""
        # very bad fix please improve if u can
        if len(args) == 1:
            args = args[0].split(" ")
        if pipeData:
            lines.append(pipeData)
        else:
            for a in args:
                try:
                    with open(a, "r") as f:
                        lines.append(f.read())
                        if "\n" not in lines[-1]:
                            lines[-1] += "\n"
                except FileNotFoundError:
                    print(f"File {a} not found")
                    return
            if lines and lines[-1][-1] == "\n":
                lines[-1] = lines[-1][:-1]
        for line in lines:
            result += line.rstrip() + "\n"
        return result
