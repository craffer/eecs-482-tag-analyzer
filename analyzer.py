"""Analyze time spent on a project using git tags."""

import sys
import datetime


def get_datetime(date_str):
    """Convert compilation git tag to the date and time of the compilation."""
    return datetime.datetime.strptime(date_str, 'compile-%Y.%m.%d_%H.%M.%S')


def get_hours(time):
    """Convert timedelta object to number of hours, rounded to 2 decimal places."""
    return format(time.total_seconds() / 3600, '.2f')

def stylized_timedelta(time):
    """Convert timedelta to a more stylized output."""
    return f"{time.days} days, {time.seconds // 3600} hours, and {time.seconds % 3600 // 60} minutes"

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

    # we aren't sure if it is possible for tags to be out of order, so this is just a precaution
    compile_times = sorted(compile_times)
    coding_sessions = []

    session_start = compile_times[0]
    prev_compile_time = session_start
    max_break = datetime.timedelta()
    for i in range(1, len(compile_times)):
        curr_compile_time = compile_times[i]
        # if you took a 1 hour 45 minute break or so between compiles we consider that a long enough
        # break to split it into two sessions (this is very arbitrary)
        if curr_compile_time - prev_compile_time > datetime.timedelta(hours=1.75):
            max_break = max(max_break, curr_compile_time - prev_compile_time)
            if session_start == prev_compile_time:
                # assume a ~20 minute session if we only compiled once
                coding_sessions.append(datetime.timedelta(minutes=20))
            else:
                # assume you worked ~10 minutes before your first compile and your last compile
                # signifies the end of your session
                coding_sessions.append(prev_compile_time - (session_start - datetime.timedelta(minutes=10)))
            session_start = curr_compile_time
        prev_compile_time = curr_compile_time
    # add the last session to our list
    coding_sessions.append(prev_compile_time - (session_start - datetime.timedelta(minutes=10)))

    total_time = sum(coding_sessions, datetime.timedelta())
    max_time = max(coding_sessions)
    mean_time = total_time / len(coding_sessions)
    median_time = sorted(coding_sessions.copy())[len(coding_sessions) // 2]
    total_elapsed = compile_times[-1] - compile_times[0]

    print(f"\nTotal time spent coding: {total_time} ({get_hours(total_time)} hours)")
    print(f"Max time spent coding in a single session: {max_time} ({get_hours(max_time)} hours)")
    print(f"Mean time spent coding per session: {mean_time} ({get_hours(mean_time)} hours)")
    print(f"Median time spent coding per session: {median_time} ({get_hours(median_time)} hours)")
    print(f"Max time spent between sessions: {max_break} ({get_hours(max_break)} hours)")
    print(f"Total time between start and end of project: {total_elapsed} ({get_hours(total_elapsed)} hours)\n")


if __name__ == "__main__":
    main()
