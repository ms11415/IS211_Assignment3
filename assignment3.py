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
    hour_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0,
                 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0,
                 22:0, 23:0}
    for row in contents:
        # counter for total number of hits
        total_hits += 1
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
        # format datetime column to datetime object
        row[1] = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        # count hits per hour
        if row[1].hour in hour_dict:
            hour_dict[row[1].hour] += 1

    image_dict = {'Total Hits':total_hits, 'Image Requests':image}
    browser_dict = {'Chrome':chrome, 'Internet Explorer':internet_explorer,
            'Firefox':firefox, 'Safari':safari}
    return [image_dict, browser_dict, hour_dict]

def displayResults(results):
    """Displays the usage information."""

    image_dict = results[0]
    browser_dict = results[1]
    hour_dict = results[2]
    popular = max(browser_dict, key=browser_dict.get)

    print '-' * 80
    print 'Image results account for {}% of all requests ({} hits)'.format(
        (100*image_dict.get('Image Requests')/image_dict.get('Total Hits')),
        image_dict.get('Total Hits'))
    print '-' * 80
    for k,v in browser_dict.iteritems():
        print '{} had {} hits'.format(k, v)
    print '-' * 80
    print '{} is the most popular browser of the day with {} hits'.format(
        popular, browser_dict.get(popular))
    print '-' * 80
    for s in sorted(hour_dict, key=hour_dict.get, reverse=True):
        print 'Hour {} had {} hits'.format(s, hour_dict[s])

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