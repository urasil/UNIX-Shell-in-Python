import re


class Sed:
    def eval(self, args, pipeData):
        if (len(args) != 2 and not pipeData) or (pipeData and len(args) != 1):
            raise ValueError("wrong number of command line arguments")

        sedCommand = args[0].strip()
        try:
            if "/" in sedCommand:
                sedCommandList = sedCommand.split("/")
            else:
                sedCommandList = sedCommand.split("|")
        except ValueError:
            raise ValueError("Invalid sed command")

        if sedCommandList[0] != "s":
            raise ValueError("Invalid sed command")

        sedCommandList.pop(0)

        if sedCommandList[-1] == "":
            sedCommandList.pop()

        if (
            len(sedCommandList) != 2 and
            not (len(sedCommandList) == 3 and sedCommandList[-1] == "g")
        ):
            raise ValueError("Invalid sed command")

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
                raise ValueError("Invalid argument format")

        except Exception as e:
            raise ValueError(f"Error executing sed command: {e}")

        for line in inputData.split("\n"):
            if gFlag:
                result += re.sub(pattern, replacement, line) + "\n"
            else:
                result += re.sub(pattern, replacement, line, 1) + "\n"

        result = result.rstrip("\n") + "\n"
        return result
