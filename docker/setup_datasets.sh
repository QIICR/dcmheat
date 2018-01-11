#!/bin/sh

DATA_ROOT=/usr/data
mkdir -p ${DATA_ROOT}

DATASET=QIN-PROSTATE-001-t2ax

DATA_LOCATION=${DATA_ROOT}/${DATASET}
cd /usr/data && curl -c -v -L http://slicer.kitware.com/midas3/download/item/126192/5-AX_T2.zip > ${DATA_ROOT}/temp.zip && unzip ${DATA_ROOT}/temp.zip && mv ${DATA_ROOT}/5-AX_T2 ${DATA_LOCATION} && rm -rf ${DATA_ROOT}/temp.zip
