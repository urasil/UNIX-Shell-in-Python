import os


class Cd:
    def eval(self, args, pipeData):
        if len(args) == 0 or len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        try:
            os.chdir(args[0])
            return ""
        except OSError as e:
            raise OSError(f"Error changing directory to {args[0]}: {e}")
