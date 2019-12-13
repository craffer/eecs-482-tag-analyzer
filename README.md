# EECS 482 Git Tag Analyzer

Perform an analysis of git tags for EECS 482 projects to determine the amount of time a group spent coding a given project.

## Usage

Run `python3 analyzer.py GIT_REPO` using a link to a repo containing a tag for each compilation. The user must also have access to this repo. For example, for statistics on EECS 482 Project 2, the user would run:

```bash
python3 analyzer.py git@github.com:eecs482/uniqname1.uniqname2.uniqname3.2
```

The user must have Python 3.7 installed on their machine.

## How It Works

A list of chronological compile tags are gathered and analyzed in an attempt to piece together how long a group worked on a project. We compare the time delta between compile tag timestamps to try and determine the length of a "session." We define a session as a (mostly) uninterrupted portion of time that a group spent coding.

When comparing time between compiles we assume that a gap of 1.75 hours or more implies that a group took a break from coding, signifying different sessions. Using this method to seperate compile tags by "session" we can compare the first timestamp with the last timestamp in a session to get the elapsed time spent coding.

### Assumptions We Make

1. Any gap between compiles that measures 1 hours and 45 minutes or greater signifies two seperate coding sessions. This is probably our largest assumption and tends to have the greatest effect on estimated time your group spent. Feel free to tweak this number to fit your personal experience.

2. Groups will tend to work *around* 10 minutes coding in total before they compile for the first time and after they compile for the last time. This assumption does not usually have a large effect on total time unless you group did a lot of small sessions.

3. Any session with only 1 compile took around 20 minutes. This is another arbitrary assumption based off of our personal experience.

4. Your group did not write an automated testing suite that recompiles constantly and runs on caen while you are not working/coding. Obviously, this would fudge the numbers.

5. Groups worked together on the project. If your group did a lot of seperate individual development that happened to line up one after another, the program will consider all of these sequential invidiual sessions as one huge session. If this is the case then you should consider dividing all of the metrics by the number of groupmates you had.

6. These numbers obviously do not consider time spent doing conceptual planning, drawing state diagrams, etc. In general, this method **tends** to underestimate time spent coding, but based off of anecdotal testing seems to line up with our percieved time spent coding on each project fairly well.
