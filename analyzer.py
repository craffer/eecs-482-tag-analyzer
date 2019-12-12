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

    compile_times = []

    # convert the file into a list of compilation times that Python can understand
    for line in tag_file:
        if line.startswith("compile-"):
            compile_times.append(get_datetime(line.strip()))
        elif line.startswith("submission-"):
            # do nothing for now
            pass
        elif line != "":
            print(f"{filename} isn't in the correct format. Try again.")
            print(line)
            sys.exit(1)

    compile_times = sorted(compile_times)
    coding_sessions = []

    session_start = compile_times[0]
    prev_compile_time = session_start + datetime.timedelta(minutes=25)

    for i in range(1, len(compile_times)):
        curr_compile_time = compile_times[i]
        if curr_compile_time - prev_compile_time > datetime.timedelta(hours=1):
            if session_start == prev_compile_time:
                # assume a ~20 minute session if we only compiled once
                coding_sessions.append(datetime.timedelta(minutes=25))
            else:
                # assume you worked ~10 minutes before your first compile
                coding_sessions.append(prev_compile_time - (session_start - datetime.timedelta(minutes=15)))
            session_start = curr_compile_time
        prev_compile_time = curr_compile_time

    total_time = datetime.timedelta()
    for session in coding_sessions:
        print(session)
        total_time += session

    print(f"Total time spent coding: {total_time} ({total_time.total_seconds() / 3600:.2f} hours)")


if __name__ == "__main__":
    main()
