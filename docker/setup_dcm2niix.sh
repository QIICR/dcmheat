#!/bin/sh

mkdir -p /usr/dcm2niix
cd /usr/dcm2niix && curl -c -v -L https://github.com/rordenlab/dcm2niix/releases/download/v1.0.20171215/dcm2niix_3-Jan-2018_lnx.zip > dcm2niix.zip && unzip /usr/dcm2niix/dcm2niix.zip -d /usr/dcm2niix && rm /usr/dcm2niix/dcm2niix.zip
# -o /usr/dcm2niix/dcm2niix.zip
#cd /usr/dcm2niix && unzip dcm2niix.zip && rm dcm2niix.zip
