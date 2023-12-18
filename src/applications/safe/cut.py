class Cut:
    def eval(self, args, pipeData):
        if (len(args) < 3 and not pipeData) or (pipeData and len(args) < 2):
            raise ValueError("wrong number of command line arguments")

        def merge_intervals(intervals):
            if not intervals:
                return []
            intervals.sort(key=lambda x: x[0])
            merged = [intervals[0]]
            for i in range(1, len(intervals)):
                current_start, current_end = intervals[i]
                last_start, last_end = merged[-1]
                if current_start <= last_end:
                    merged[-1] = (last_start, max(last_end, current_end))
                else:
                    merged.append(intervals[i])
            return merged
        lines = []
        if args[0] != "-b":
            raise ValueError("Only the -b option is supported")
        else:
            try:
                toCut = args[1].split(",")
                if len(args) > 2:
                    lines = open(args[2]).readlines()
                else:
                    lines = pipeData.split("\n")
            except FileNotFoundError:
                raise FileNotFoundError(f"File {args[2]} not found")
        result = ""
        if lines and lines[-1] == "":
            # will only pop when pipeData not None
            lines.pop()
        for line in lines:
            temp_range = []
            for brange in toCut:
                if "-" in brange:
                    start, end = brange.split("-")
                    start = int(start) - 1 if start else 0
                    end = int(end) if end else len(line)
                else:
                    start = int(brange) - 1
                    end = start + 1
                temp_range.append((start, end))
            merged = merge_intervals(temp_range)
            for start, end in merged:
                temp_line = line[start:end]
                result += temp_line.rstrip("\n")
            result += "\n"

        return result
