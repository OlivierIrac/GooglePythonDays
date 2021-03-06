#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    f = open(filename, "rU")
    text = f.read()
    f.close()
    namesList = []
    # year = re.search(r'<h3 align="center">Popularity in (\d\d\d\d)</h3>', text)
    # namesList.append(year.group(1))
    finds = re.findall(r'<tr align="right"><td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', text)
    for find in finds:
        namesList.append((find[1], find[0]))
        namesList.append((find[2], find[0]))
    # remove duplicates, keep only highest rank
    namesList.sort()
    lastName = (None, None)
    for name in namesList:
        if name[0] == lastName[0]:
            if int(name[1]) < int(lastName[1]):
                namesList.remove(lastName)
            else:
                namesList.remove(name)
        lastName = name
    return namesList


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print 'usage: [--summaryfile] file [file ...]'
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    for filename in args:
        namesList = extract_names(filename)
        if summary:
            f = open(filename + ".summary", "w")
            for item in namesList:
                f.write(item[0] + ' ' + item[1] + '\n')
            f.close()
        else:
            for item in namesList:
                print item[0] + ' ' + item[1]


if __name__ == '__main__':
    main()
