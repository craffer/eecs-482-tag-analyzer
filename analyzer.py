"""Analyze time spent on a project using git tags."""

import sys
import subprocess
import re
import datetime


def get_datetime(line):
    """Convert compilation git tag to the date and time of the compilation."""
    rgx = r"refs\/tags\/compile-(\d{4}\.\d{2}\.\d{2}_\d{2}\.\d{2}\.\d{2})"
    date_str = re.search(rgx, line).group(1)
    if not date_str:
        raise Exception('get_datetime failed')
    return datetime.datetime.strptime(date_str, '%Y.%m.%d_%H.%M.%S')


def get_hours(time):
    """Convert timedelta object to number of hours, rounded to 2 decimal places."""
    return format(time.total_seconds() / 3600, '.2f')


def stylized_timedelta(time):
    """Convert timedelta to a more stylized output."""
    return f"{time.days} days, {time.seconds // 3600} hours, " +\
           f"and {time.seconds % 3600 // 60} minutes"


def print_metric(message, time, just_hours=False):
    """Print out a metric given a message to print and a timedelta."""
    if (just_hours):
        print(f"{message}: {get_hours(time)} hours")
    else:
        print(f"{message}: {stylized_timedelta(time)} ({get_hours(time)} hours)")


def main():
    """Run the analyzer."""
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} REPO_LINK")
        sys.exit(1)

    repo = sys.argv[1]
    fetch_tags = ["git", "ls-remote", "--tags", repo]
    command_result = subprocess.run(fetch_tags, capture_output=True, text=True)
    if command_result.returncode != 0:
        print(f"{repo} isn't valid. Try again.")
        sys.exit(1)
    tags = command_result.stdout

    compile_times = []

    # convert the file into a list of compilation times that Python can understand
    for line in tags.splitlines():
        if 'refs/tags/compile-' in line:
            try:
                compile_times.append(get_datetime(line.strip()))
            except Exception:
                print(f"{repo} isn't valid. Try again.")
                sys.exit(1)
        elif 'refs/tags/submission-' in line:
            # do nothing for now
            pass
        elif line != "":
            print(f"{repo} isn't valid. Try again.")
            sys.exit(1)

    # we aren't sure if it is possible for tags to be out of order, so this is just a precaution
    compile_times = sorted(compile_times)
    coding_sessions = []

    session_start = compile_times[0]
    prev_compile_time = session_start
    max_break = datetime.timedelta()
    for i in range(1, len(compile_times)):
        curr_compile_time = compile_times[i]
        # if you took a 1 hour 45 minute break or so between compiles we consider that a big enough
        # break to split it into two sessions (this is very arbitrary)
        if curr_compile_time - prev_compile_time > datetime.timedelta(hours=1.75):
            max_break = max(max_break, curr_compile_time - prev_compile_time)
            if session_start == prev_compile_time:
                # assume a ~20 minute session if we only compiled once
                coding_sessions.append(datetime.timedelta(minutes=20))
            else:
                # assume you worked ~10 minutes before your first compile and your last compile
                # signifies the end of your session
                coding_sessions.append(prev_compile_time -
                                       (session_start - datetime.timedelta(minutes=10)))
            session_start = curr_compile_time
        prev_compile_time = curr_compile_time
    # add the last session to our list
    coding_sessions.append(prev_compile_time - (session_start - datetime.timedelta(minutes=10)))

    total_time = sum(coding_sessions, datetime.timedelta())
    max_time = max(coding_sessions)
    mean_time = total_time / len(coding_sessions)
    median_time = sorted(coding_sessions.copy())[len(coding_sessions) // 2]
    total_elapsed = compile_times[-1] - compile_times[0]
    percent_coding = total_time / total_elapsed

    print_metric("\nTotal time spent coding", total_time)
    print("")
    print_metric("Longest coding session", max_time, True)
    print_metric("Mean time spent coding per session", mean_time, True)
    print_metric("Median time spent coding per session", median_time, True)
    print_metric("Longest break between sessions", max_break)
    print_metric("Total time between start/end of project", total_elapsed)
    print(f"Percentage of your life spent coding in between when you started and when you " +
          f"finished: {percent_coding * 100:.2f}%\n")


if __name__ == "__main__":
    main()
