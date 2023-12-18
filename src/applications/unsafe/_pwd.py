import os


class _Pwd:
    def eval(self, args, pipeData):
        if len(args) != 0:
            print("wrong number of command line arguments")
            return
        result = os.getcwd()
        return result
