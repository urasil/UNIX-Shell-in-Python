import regex


class _Grep:
    def eval(self, args, pipeData):
        # Check if the -i flag is present
        case_insensitive = '-i' in args
        # Remove the -i flag from the arguments list if present
        if case_insensitive:
            args.remove('-i')

        if (len(args) < 2 and not pipeData) or (pipeData and len(args) > 1):
            print("wrong number of command line arguments")
            return

        pattern = args[0]
        files = []
        if not pipeData:
            files = args[1:]

        if pattern.startswith("'") and pattern.endswith("'"):
            # Remove the quotes and escape the dots to match them literally
            pattern = pattern[1:-1].replace('.', r'\.')

        # Compile the regex with regex.IGNORECASE if the -i flag is present
        if case_insensitive:
            regex_pattern = regex.compile(pattern, regex.IGNORECASE)
        else:
            regex_pattern = regex.compile(pattern)

        result = ""
        if not pipeData:
            for file in files:
                try:
                    # If file is not an empty string, open the file
                    if file:
                        with open(file, 'r') as f:
                            lines = f.readlines()

                    for line in lines:
                        # Search for the pattern
                        if regex_pattern.search(line):
                            formatted_line = line.rstrip()
                            """
                            If there are multiple files or
                            reading from stdin, prefix with the file name
                            """
                            if len(files) > 1 or not file:
                                prefix = f"{file}:" if file else ""
                                result += f"{prefix}{formatted_line}"
                            else:
                                result += formatted_line
                            # Append a blank line after each match
                            result += '\n'

                except IOError as e:
                    print(f"Error opening or reading file {file}: {e}")
                    return
        else:
            lines = pipeData.split("\n")
            for line in lines:
                # Search for the pattern
                if regex_pattern.search(line):
                    formatted_line = line.rstrip()
                    result += formatted_line.rstrip("\n") + "\n"
        return result
