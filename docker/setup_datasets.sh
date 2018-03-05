#!/bin/sh

DATA_ROOT=/usr/data
mkdir -p ${DATA_ROOT}

#cd /usr/data && curl -c -v -L http://slicer.kitware.com/midas3/download/item/126192/5-AX_T2.zip > ${DATA_ROOT}/temp.zip && unzip ${DATA_ROOT}/temp.zip && mv ${DATA_ROOT}/5-AX_T2 ${DATA_LOCATION} && rm -rf ${DATA_ROOT}/temp.zip
cd $DATA_ROOT && curl -L https://www.dropbox.com/s/h75cttxculzcvbt/dcmheat.zip?dl=1 > ${DATA_ROOT}/dcmheat.zip && unzip dcmheat.zip
