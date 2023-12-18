import re


class _Sed:
    def eval(self, args, pipeData):
        if (len(args) != 2 and not pipeData) or (pipeData and len(args) != 1):
            print("wrong number of command line arguments")
            return

        sedCommand = args[0].strip()
        try:
            if "/" in sedCommand:
                sedCommandList = sedCommand.split("/")
            else:
                sedCommandList = sedCommand.split("|")
        except ValueError:
            print("Invalid sed command")
            return

        if sedCommandList[0] != "s":
            print("Invalid sed command")
            return

        sedCommandList.pop(0)

        if sedCommandList[-1] == "":
            sedCommandList.pop()

        if (
            len(sedCommandList) != 2 and
            not (len(sedCommandList) == 3 and sedCommandList[-1] == "g")
        ):
            print("Invalid sed command")
            return

        pattern = sedCommandList[0]
        replacement = sedCommandList[1]
        gFlag = len(sedCommandList) == 3

        result = ""
        try:
            if pipeData:
                inputData = pipeData
            elif len(args) == 2:
                with open(args[1], 'r') as f:
                    inputData = f.read()
            else:
                print("Invalid argument format")
                return

        except Exception as e:
            print(f"Error executing sed command: {e}")
            return

        for line in inputData.split("\n"):
            if gFlag:
                result += re.sub(pattern, replacement, line) + "\n"
            else:
                result += re.sub(pattern, replacement, line, 1) + "\n"

        result = result.rstrip("\n") + "\n"
        return result
