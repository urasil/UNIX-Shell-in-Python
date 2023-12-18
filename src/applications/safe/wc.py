class Wc:
    def eval(self, args, pipeData):
        if (len(args) < 1 and not pipeData) or (pipeData and len(args) != 0):
            raise ValueError("wrong number of command line arguments")
        clean = []
        for arg in args:
            tmp = arg.split(" ")
            clean.extend(tmp)
        args = clean
        flag = None
        if args[0] == '-m' or args[0] == '-w' or args[0] == '-l':
            flag = args.pop(0)

        fileContent = ""
        if not pipeData:
            for _file in args:
                try:
                    with open(_file, 'r') as f:
                        fileContent += f.read()
                        fileContent = fileContent.rstrip("\n") + "\n"
                except FileNotFoundError as e:
                    raise FileNotFoundError(f"File {args[0]} not found: {e}")
        else:
            fileContent = pipeData

        countBytes = len(fileContent.encode('utf-8'))
        countWords = len(fileContent.split())
        countLines = len(fileContent.splitlines())
        result = f"{countLines} {countWords} {countBytes}"

        # Check for flags
        if flag:
            if flag == '-m':
                result = f"{countBytes}"
            elif flag == '-w':
                result = f"{countWords}"
            elif flag == '-l':
                result = f"{countLines}"
            else:
                raise ValueError(f"Unknown flag: {flag}")

        result += "\n"
        return result
