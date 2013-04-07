#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import fileinput
from sys import stdout

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

def to_google(s):
    t = s.split('.')
    return int(t[0][:-2]) + (int(t[0][-2:]) + int(t[1]) / (10.0 ** len(t[1]))) / 60

def convert(input):
    result = []
    for s in input:
        t = s.rstrip('\r\n').split(',')
        if t[0] != '$GPGGA':
            continue
        result.append('%.7f,%.7f,%s' % (to_google(t[4]), to_google(t[2]), t[9]))
    return result

def write_output(points):
    stdout.write(template_before)
    stdout.write('      <LineString><coordinates>%s</coordinates></LineString>\n' % ' '.join(points))
    stdout.write(template_after)

def main(argv):
    write_output(convert(fileinput.input()))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
