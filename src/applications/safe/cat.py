class Cat:
    def eval(self, args, pipeData):
        # print("cat eval")
        lines = []
        result = ""
        clean = []
        for arg in args:
            tmp = arg.split(" ")
            clean.extend(tmp)
        args = clean
        if pipeData:
            lines.append(pipeData)
        else:
            for a in args:
                try:
                    with open(a, "r") as f:
                        lines.append(f.read())
                        if "\n" not in lines[-1][-1]:
                            lines[-1] += "\n"
                except FileNotFoundError:
                    raise FileNotFoundError(f"File {a} not found")
        for line in lines:
            result += line.rstrip() + "\n"
        return result
