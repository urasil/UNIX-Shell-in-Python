import os


class _Cd:
    def eval(self, args, pipeData):
        if len(args) == 0 or len(args) > 1:
            print("wrong number of command line arguments")
            return
        try:
            os.chdir(args[0])
            return ""
        except OSError as e:
            print(f"Error changing directory to {args[0]}: {e}")
            return
