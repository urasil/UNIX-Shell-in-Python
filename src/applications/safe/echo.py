import os


class Echo:
    def eval(self, args, pipeData):
        tmpList = []
        for arg in args:
            if "*" in arg:
                _dir, _, pattern = arg.rpartition("/")
                if not _dir:
                    _dir = "."
                pre, _, suf = pattern.partition("*")
                for _file in os.listdir(_dir):
                    if _file.startswith(pre) and _file.endswith(suf):
                        if _dir != ".":
                            tmpList.append(os.path.join(_dir, _file))
                        else:
                            tmpList.append(_file)
            else:
                tmpList.append(arg)

        result = " ".join(tmpList).rstrip("\n") + "\n"
        return result
