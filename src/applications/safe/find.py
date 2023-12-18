import os
import fnmatch


class Find:
    def eval(self, args, pipeData):
        if (len(args) < 2):
            raise ValueError("wrong number of command line arguments")

        # Default to current directory if PATH not specified
        path = args[0] if len(args) > 2 else '.'
        if '-name' in args and len(args) > args.index('-name') + 1:
            pattern = args[args.index('-name') + 1]
        else:
            pattern = None

        # Validate input
        if not os.path.exists(path):
            raise FileNotFoundError(f"Error: Path '{path}' does not exist.\n")

        # only accepts path -name pattern and -name pattern
        if not pattern:
            raise ValueError("Please provide a file name pattern with -name option.\n")

        result = ""
        # Recursively search for files with matching names
        for root, dirs, files in os.walk(path):
            for file in fnmatch.filter(files, pattern):
                relative_path = os.path.join(root, file)
                string = f"{relative_path}"
                result += string.rstrip("\n") + "\n"

        return result
