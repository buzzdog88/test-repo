#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Conversion of Global Coherence Initiative binary magnetometer data.
Contact: Mark Dammer (info@mdammer.net)
Data structure format:
140 byte header
1) Integer size in bytes.   (LONG  4-byte Signed Integer)
2) Hostname char[128]       (unsigned byte) 
3) Num_lines                (LONG  4-byte Signed Integer)
4) Sampling Rate            (LONG  4-byte Signed Integer)

32 byte datablocks
1) point_number             (LONG  4-byte Signed Integer)
2) A/D ch0   N/S            (LONG  4-byte Signed Integer)
3) A/D ch1   E/W            (LONG  4-byte Signed Integer)
4) A/D ch2   Vert           (LONG  4-byte Signed Integer)
5) A/D ch3   NC             (LONG  4-byte Signed Integer)
6) time_seconds             (DOUBLE 8-byte Float int Point)
7) Temp (°F)                (LONG 4-byte Signed Integer)

"""

import struct
import sys

optionlen = len(sys.argv)
if (optionlen > 1):
    filepattern = sys.argv[1:]
else:
    print 'Missing argument (filename or pattern)'
    sys.exit()

for gci_filename in filepattern:
    gci_file = open(gci_filename)
    gci_data = gci_file.read()
    gci_header = struct.unpack('<l128sll',gci_data[0:140])
    gci_data_start = 140
    gci_mags = []
    gci_data_stop = gci_data_start + (gci_header[2] - 1)*32
    print '#Integer size (bytes): ' + str(gci_header[0])
    print '#Hostname: ' + str(gci_header[1])
    print '#Num_Lines: ' + str(gci_header[2])
    print '#Sampling Rate: ' + str(gci_header[3])
    print '#point, NS(pT), EW(pT), Vert(pT), time(Sec), temp(F)'
    for sample_index in xrange(gci_data_start,gci_data_stop,32):
        gci_dataset = struct.unpack('<llllldl',gci_data[sample_index:sample_index + 32])
        print str(gci_dataset[0])+','+str(gci_dataset[1]/1048.576)+','+str(gci_dataset[2]/1048.576)+','+str(gci_dataset[3]/1048.576)+','+str(gci_dataset[5])+','+str(gci_dataset[6])
    gci_file.close



