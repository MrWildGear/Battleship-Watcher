def filter_lines_by(lines: list, filter_word: str) -> list:
    """ cleans the parameter lines and returns a clean list
    :param filter_word: string
    :param lines: list of strings
    :returns a filtered list of strings
    """
    clean_lines = []
    for line in lines:
        if line.__contains__(filter_word):
            clean_lines.append((line.split("-"))[0])
    return clean_lines


def read_file(filename) -> list:
    """ opens the file of the directory 'filename' and returns all the lines in a list
    :param filename : is a file directory string
    :returns a list of strings"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise Exception("File not found")
    return lines
