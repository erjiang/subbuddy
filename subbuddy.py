from __future__ import print_function
import sys
from datetime import datetime, timedelta
"""
Helps you record subtitles in real-time.

Usage: python subbuddy.py > outputfile.srt

1. Press Enter when video recording starts.
2. Type each line followed by Enter.
3. When done, give it EOF (Ctrl-D on some systems).

You may need to correct the offset of the subtitles using some other programs.

@author Eric Jiang <eric@doublemap.com>
"""

subs = []


def main():
    sys.stderr.write("Awaiting your Enter key...")
    sys.stdin.readline()  # eat newline

    # begin recording
    start_time = datetime.now()
    last_time = timedelta()
    sys.stderr.write("[%s] " % format_timestamp(last_time))
    while True:
        line = sys.stdin.readline()
        if not line:  # EOF
            break

        # record this line and time
        subs.append({
            "time": last_time,
            "line": line.strip()
        })
        # set up next recording
        last_time = datetime.now() - start_time
        sys.stderr.write("[%s] " % format_timestamp(last_time))

    for idx, sub in enumerate(subs):
        # try to figure out how long to display the sub
        # either double the est. reading time or the next line's time,
        # whichever is less
        end_time = sub['time'] + estimate_duration(sub['line']) * 2
        if idx < len(subs) - 1:
            next_sub = subs[idx + 1]
            if next_sub['time'] < sub['time'] + end_time:
                end_time = next_sub['time']
        print(idx + 1)
        print("%s --> %s" % (
            format_timestamp(sub["time"]),
            format_timestamp(end_time)))
        print(sub["line"])
        print()


def estimate_duration(txt):
    """Estimate how long a string takes to read."""
    return timedelta(seconds=(len(txt) / 10))


def format_timestamp(td):
    """TODO: fix for timedeltas greater than one day"""
    hh, rem = divmod(td.seconds, 3600)
    mm, rem = divmod(rem, 60)
    ss, _ = divmod(rem, 1)
    return "%02d:%02d:%02d,%03d" % (hh, mm, ss, td.microseconds / 1000)


if __name__ == "__main__":
    main()
