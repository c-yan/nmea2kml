#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fileinput import input as finput
from sys import argv, exit, stdout

template_before = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
<Document>
  <name>Track Log</name>
  <description>Route</description>
  <Style id="roadStyle">
    <LineStyle>
      <color>ff4444ff</color>
      <width>3</width>
    </LineStyle>
  </Style>
  <Placemark>
    <name>Route</name>
    <styleUrl>#roadStyle</styleUrl>
    <MultiGeometry>\n'''

template_after = '''    </MultiGeometry>
  </Placemark>
</Document>
</kml>\n'''

# dddmm.mmmm -> ddd.dddd
def to_google(s):
    i = s.find('.')
    return int(s[:i - 2]) + float(s[i - 2:]) / 60

def convert(input):
    result = []
    for s in input:
        t = s.rstrip('\r\n').split(',')
        if len(t) != 15 or t[0] != '$GPGGA' or t[2] == '' or t[4] == '' or t[9] == '':
            continue
        result.append('%.7f,%.7f,%s' % (to_google(t[4]), to_google(t[2]), t[9]))
    return result

def write_output(points):
    stdout.write(template_before)
    stdout.write('      <LineString><coordinates>%s</coordinates></LineString>\n' % ' '.join(points))
    stdout.write(template_after)

def main(argv):
    write_output(convert(finput()))

if __name__ == "__main__":
    exit(main(argv))
