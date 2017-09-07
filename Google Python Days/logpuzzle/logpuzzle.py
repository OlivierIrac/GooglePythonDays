#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    f = open(filename, "rU")
    text = f.read()
    f.close()
    URLsList = []
    # year = re.search(r'<h3 align="center">Popularity in (\d\d\d\d)</h3>', text)
    # namesList.append(year.group(1))
    finds = re.findall(r'GET (\S*puzzle\S*.jpg) ', text)
    for find in finds:
        imageName = find.split('/')[-1]
        URLsList.append('https://developers.google.com/edu/python/images/puzzle/' + imageName)
    # remove duplicates, keep only highest rank
    URLsList.sort()
    lastURL = ''
    for URL in URLsList:
        if URL == lastURL:
            URLsList.remove(URL)
        lastURL = URL
    return URLsList


def download_images(img_urls, todir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    imgIndex = 0
    if len(todir):
        if (not os.path.exists(todir)):
            os.makedirs(todir)
    for url in img_urls:
        imgFilename = os.path.join(todir, 'img' + str(imgIndex) + '.jpg')
        print 'Downloading ' + imgFilename + ' from: ' + url
        urllib.urlretrieve(url, imgFilename)
        imgIndex += 1
    f = open(os.path.join(todir, 'index.html'), "w")
    f.write("<html><body>")
    for i in range(imgIndex):
        f.write("<img src=\"img" + str(i) + ".jpg\">")
    f.write("</body></html>")
    f.close()


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)


if __name__ == '__main__':
    main()
