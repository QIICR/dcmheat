#!/bin/sh

# Slicer 4.8.1
SLICER_URL="http://download.slicer.org/bitstream/738960"
curl -v -s -L $SLICER_URL | tar xz -C /tmp
mv /tmp/Slicer* /usr/slicer
