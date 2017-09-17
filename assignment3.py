#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 Assignment 3."""

from __future__ import division
import argparse
import csv
import datetime
import re
import urllib2

def downloadData(urlname):
    """Downloads contents at specified url and returns a CSV reader object."""
    # http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
    response = urllib2.urlopen(urlname)
    data = csv.reader(response)
    return data

def processData(contents):
    """Processes the CSV data line by line, sums and returns dictionary of
    image hits (gif, png, jpg and jpeg), browser hits and total hits.
    """
    total_hits = 0
    image = 0
    chrome = 0
    internet_explorer = 0
    firefox = 0
    safari = 0
    for row in contents:
        # searches for image hits
        if re.search('jpg|jpeg|gif|png', row[0], re.IGNORECASE):
            image += 1
        # searches for browser types
        if re.search('Chrome', row[2]):
            chrome += 1
        elif re.search('MSIE', row[2]):
            internet_explorer +=1
        elif re.search('Firefox', row[2]):
            firefox += 1
        elif re.search('Safari', row[2]):
            safari += 1
        #counter for total number of hits
        total_hits += 1
    image_dict = {'Total Hits':total_hits, 'Image Requests':image}
    browser_dict = {'Chrome':chrome, 'Internet Explorer':internet_explorer,
            'Firefox':firefox, 'Safari':safari}
    return [image_dict, browser_dict]

def displayResults(results):
    """Displays the usage information."""

    image_dict = results[0]
    browser_dict = results[1]
    popular = max(browser_dict, key=browser_dict.get)

    print 'Image results account for {}% of all requests'.format(
        (100*image_dict.get('Image Requests')/image_dict.get('Total Hits'))
    )
    print '{} is the most popular browser of the day'.format(popular)

def main():
    """Main function."""
    # Parses required URL argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()
    url = args.url
    # Downloads data and assigns it to csv_data
    csv_data = downloadData(url)
    # csv_data is processed
    results = processData(csv_data)
    # prints results
    displayResults(results)

if __name__ == "__main__":
    main()