import os


class Pwd:
    def eval(self, args, pipeData):
        if len(args) != 0:
            raise ValueError("wrong number of command line arguments")
        result = os.getcwd()
        return result
