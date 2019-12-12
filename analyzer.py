"""Analyze time spent on a project using git tags."""

import sys
import datetime


def get_datetime(date_str):
    """Convert compilation git tag to the date and time of the compilation."""
    return datetime.datetime.strptime(date_str, 'compile-%Y.%m.%d_%H.%M.%S')


def main():
    """Run the analyzer."""
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} tag_file")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        tag_file = open(filename)
    except OSError:
        print(f"Couldn't open file {filename}. Try again.")
        sys.exit(1)

    for line in tag_file:
        if line.startswith("compile-"):
            compile_time = get_datetime(line.strip())
        elif line.startswith("submission-"):
            pass
        elif line != "":
            print(f"{filename} isn't in the correct format. Try again.")
            print(line)
            sys.exit(1)


if __name__ == "__main__":
    main()
