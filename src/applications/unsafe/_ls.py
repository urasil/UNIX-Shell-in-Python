from os import listdir
import os


class _Ls:
    def eval(self, args, pipeData):
        result = ""
        if len(args) == 0 and not pipeData:
            ls_dir = os.getcwd()
        elif len(args) == 0 and pipeData:
            ls_dir = pipeData.rstrip("\n")
            ls_dir = ls_dir.strip()
        elif len(args) > 1:
            print("wrong number of command line arguments")
            return
        else:
            ls_dir = args[0]
        if os.path.exists(ls_dir) and os.path.isdir(ls_dir):
            for f in listdir(ls_dir):
                if not f.startswith("."):
                    result += f + "\n"
        else:
            print(f"The directory '{ls_dir}' does not exist.")
            return
        return result
