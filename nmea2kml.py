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
  <Style id="blueDot">
    <IconStyle>
      <Icon>
        <href>http://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png</href>
      </Icon>
    </IconStyle>
  </Style>
  <Placemark>
    <name>Route</name>
    <styleUrl>#roadStyle</styleUrl>
    <MultiGeometry>\n'''

template_middle = '''    </MultiGeometry>
  </Placemark>
  <Folder>
    <name>waypoints</name>\n'''

template_after = '''  </Folder>
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
        result.append((t[1], to_google(t[4]), to_google(t[2]), t[9]))
    return result

def write_output(points):
    stdout.write(template_before)
    stdout.write('      <LineString><coordinates>%s</coordinates></LineString>\n' % ' '.join('%.7f,%.7f,%s' % p[1:] for p in points))
    stdout.write(template_middle)
    t = ''
    for p in points:
        if p[0][:4] == t:
            continue
        t = p[0][:4]
        stdout.write('    <Placemark>\n')
        stdout.write('      <name>%s</name>\n' % ('%s:%s' % (t[:2], t[2:])))
        stdout.write('      <styleUrl>#blueDot</styleUrl>\n')
        stdout.write('      <Point><coordinates>%s</coordinates></Point>\n' % ('%.7f,%.7f,%s' % p[1:]))
        stdout.write('    </Placemark>\n')
    stdout.write(template_after)

def main(argv):
    write_output(convert(finput()))

if __name__ == "__main__":
    exit(main(argv))
