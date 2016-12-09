from enum import Enum


class State(Enum):
    CODE = 1
    C_COMMENT = 2
    CPP_COMMENT = 3
    STRING_LITERAL = 4


def filter_java_comment(text):
    """ Removes Java (C/C++) style comments from text. """
    result = []  # filtered text (char array)
    prev = ''  # previous char
    prevprev = ''  # previous previous char
    state = State.CODE

    for ch in text:
        # Skip to the end of C-style comment
        if state == State.C_COMMENT:
            if prevprev != '\\' and prev == '*' and ch == '/':  # End comment
                state = State.CODE
                prevprev = prev = ''
            elif ch == '\n':
                result.append('\n')
                prevprev = prev = ''
            else:
                prevprev, prev = prev, ch
            continue

        # Skip to the end of the line (C++ style comment)
        if state == State.CPP_COMMENT:
            if ch == '\n':  # End comment
                state = State.CODE
                result.append('\n')
                prevprev = prev = ''
            continue

        # Skip to the end of the string literal
        if state == State.STRING_LITERAL:
            if prev != '\\' and ch == '"':  # End literal
                state = State.CODE
            result.append(prev)
            prevprev, prev = prev, ch
            continue

        # Starts C-style comment?
        if prevprev != '\\' and prev == '/' and ch == '*':
            state = State.C_COMMENT
            prevprev = prev = ''
            continue

        # Starts C++ style comment?
        if prevprev != '\\' and prev == '/' and ch == '/':
            state = State.CPP_COMMENT
            prevprev = prev = ''
            continue

        # Comment has not started yet
        if prev: result.append(prev)

        # Starts string literal?
        if ch == '"':
            state = State.STRING_LITERAL
        prevprev, prev = prev, ch

    # Returns filtered text
    if prev: result.append(prev)
    return ''.join(result)


def iter_literals(text):
    """ Iterates all string literals in the text. """
    in_literal = False
    result = ''
    for ch in text:
        if in_literal:
            if ch == '"':  # End literal
                in_literal = False
                if result: yield result
            else:  # Continue literal
                result += ch
        elif ch == '"':  # Begin literal
            in_literal = True
            result = ''


if __name__ == '__main__':
    import glob
    import sys
    filename = sys.argv[1]
    for name in glob.iglob(filename, recursive=True):
        with open(name, encoding='utf-8') as f:
            for literal in iter_literals(filter_java_comment(f.read())):
                print(literal)

